import json
# a2a
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    Part,
    TaskState,
    TextPart,
)
from a2a.utils import (
    new_agent_text_message,
    new_task,
)
# adk
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
# others
from agent import root_agent


class agent_executor(AgentExecutor):
    """
    Custom AgentExecutor that streams ADK planning steps as JSON artifacts.
    Each intermediate step and the final response are sent as structured data.
    """

    def __init__(self):
        # Initialize the ADK agent from the root factory
        self.agent = root_agent
        self.status_message = 'Agent is processing...'
        self.runner = Runner(
            app_name=self.agent.name,
            agent=self.agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

    async def cancel(
            self,
            context: RequestContext,
            event_queue: EventQueue,
    ) -> None:
        """Cancel the execution of a specific task."""
        raise NotImplementedError(
            'Cancellation is not implemented for ADKAgentExecutor.'
        )

    async def execute(
            self,
            context: RequestContext,
            event_queue: EventQueue,
    ) -> None:
        """
        Execution entrypoint. Captures ReAct steps from PlanReActPlanner
        and converts them into JSON artifacts for the A2A client.
        """

        # 1. Setup Task and Context
        query = context.get_user_input()
        task = context.current_task

        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)
        user_id = context.call_context.user.user_name if context.call_context else 'a2a_user'

        try:
            # 2. Update status to working
            await updater.update_status(
                TaskState.working,
                new_agent_text_message(
                    self.status_message, task.context_id, task.id
                ),
            )

            # 3. Initialize ADK session
            session = await self.runner.session_service.create_session(
                app_name=self.agent.name,
                user_id=user_id,
                state={},
                session_id=task.context_id,
            )

            content = types.Content(
                role='user', parts=[types.Part.from_text(text=query)]
            )

            response_text = ''
            step_no = 0

            # 4. Stream events from ADK Runner
            async for event in self.runner.run_async(
                    user_id=user_id, session_id=session.id, new_message=content
            ):

                if (
                        event.is_final_response()
                        and event.author == "questions_ordering_agent"
                        and event.content
                        and event.content.parts
                ):
                    response_text = event.content.parts[0].text
                elif event.content.parts:
                    for content in event.content.parts:
                        if hasattr(content, 'text'):
                            intermediate_json = {
                                'step': 'intermediate',
                                'content': content.text,
                                'author': event.author
                            }
                            await updater.add_artifact(
                                [Part(root=TextPart(text=json.dumps(intermediate_json)))],
                                name=f"intermediate_content_{step_no}"
                            )
                            step_no += 1

            # 5. Final JSON Artifact with "finish" step
            final_json = {
                "step": "finish",
                "answer": response_text.strip(),
                "author": "questions_ordering_agent",
            }

            await updater.add_artifact(
                [Part(root=TextPart(text=json.dumps(final_json)))],
                name="final_result",
            )

            await updater.complete()

        except Exception as e:
            await updater.update_status(
                TaskState.failed,
                new_agent_text_message(
                    f'Error during execution: {e!s}', task.context_id, task.id
                ),
                final=True,
            )
