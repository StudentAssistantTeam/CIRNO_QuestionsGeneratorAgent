from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    Part,
    Task,
    TaskState,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import (
    new_agent_text_message,
    new_task,
)
from a2a.utils.errors import ServerError
import json
from agent import root_agent


class agent_executor(AgentExecutor):
    """
    Custom AgentExecutor with streaming trace support.

    This executor extends the default behavior by:
    1. Emitting structured trace steps as artifacts (for UI visualization)
    2. Preserving text streaming for chat-style updates
    3. Supporting step-by-step execution introspection (planner/tool/llm)
    """

    def __init__(self):
        # Initialize the underlying agent instance
        self.agent = root_agent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """
        Main execution entrypoint.

        This method:
        - Initializes or retrieves the current task
        - Streams agent outputs
        - Converts intermediate steps into structured trace artifacts
        - Emits final result upon completion
        """

        # Extract user input from request context
        query = context.get_user_input()

        # Retrieve current task (if exists)
        task = context.current_task

        # Create a new task if none exists (first request)
        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)

        # TaskUpdater is responsible for pushing events to frontend
        updater = TaskUpdater(event_queue, task.id, task.context_id)

        # Incremental step counter (used for ordering / DAG construction)
        step_id = 0

        # Stream results from underlying agent
        async for item in self.agent.stream(query, task.context_id):

            # Whether the agent has finished execution
            is_task_complete = item.get("is_task_complete", False)

            # =========================================
            # Handle intermediate steps (trace emission)
            # =========================================
            if not is_task_complete:

                step_id += 1

                # Build structured trace payload for frontend visualization
                trace_payload = {
                    "id": f"step_{step_id}",          # Unique step identifier
                    "type": item.get("type", "llm"),  # planner | tool | llm | subagent
                    "title": item.get("title", "Processing"),
                    "content": item.get("updates", ""),  # Human-readable description
                    "metadata": item.get("metadata", {}),  # Optional structured data
                }

                # Emit structured trace as artifact (for timeline / graph UI)
                await updater.add_artifact(
                    [
                        Part(
                            root=TextPart(
                                text=json.dumps(trace_payload, ensure_ascii=False)
                            )
                        )
                    ],
                    name="trace_step",  # Artifact channel for trace visualization
                )

                # Also emit plain text updates (for chat-style streaming UI)
                await updater.update_status(
                    TaskState.working,
                    new_agent_text_message(
                        item.get("updates", ""),
                        task.context_id,
                        task.id,
                    ),
                )

                continue

            # =========================================
            # Handle final result
            # =========================================
            await updater.add_artifact(
                [
                    Part(
                        root=TextPart(
                            text=item.get("content", "")
                        )
                    )
                ],
                name="result_question",  # Final output artifact
            )

            # Mark task as complete
            await updater.complete()
            break

    async def cancel(
        self, request: RequestContext, event_queue: EventQueue
    ) -> Task | None:
        """
        Cancellation is not supported in this executor.
        """
        raise ServerError(error=UnsupportedOperationError())
