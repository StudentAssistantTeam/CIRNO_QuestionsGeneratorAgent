import uvicorn
from logging import getLogger
import httpx
# a2a
from a2a.types import (
    AgentSkill,
    AgentCapabilities,
    AgentCard
)
from a2a.server.apps import A2AStarletteApplication
from a2a.server.tasks import (
    InMemoryPushNotificationConfigStore,
    InMemoryTaskStore,
    DatabasePushNotificationConfigStore,
    DatabaseTaskStore,
    BasePushNotificationSender
)
from a2a.server.request_handlers import DefaultRequestHandler
# project dependencies
from cirno_questions_generator_agent.agent_executor import agent_executor
from cirno_questions_generator_agent.config import settings
from cirno_questions_generator_agent.logger_config import setup_logging

logger = getLogger("server")
executor_instance = agent_executor()


# Main function
def main():
    # Capabilities
    agent_capabilities = AgentCapabilities(
        streaming=True
    )
    # Skills
    questions_generator_skill = AgentSkill(
        id="questions_generator_skill",
        name="Questions Generator Skill",
        description="Generate questions according to the request",
        examples=[
"""
{
    "topic": "Gravity",
    "has_sample_questions": false,
    "questions_number": 5
}
"""
        ],
        tags=["questions_generation"],
    )
    # Agent Card
    agent_card = AgentCard(
        name="question_generator_agent",
        url=f"http://localhost:{settings.a2a_port}/",
        description="Test agent from file",
        version="0.1.0",
        capabilities=agent_capabilities,
        skills=[
            questions_generator_skill
        ],
        default_input_modes=["application/json"],
        default_output_modes=["application/json"],
        supports_authenticated_extended_card=False
    )
    # Server
    httpx_client = httpx.AsyncClient()
    # Configuring the push notification system
    if settings.use_db_push_notifications:
        push_config_store = DatabasePushNotificationConfigStore(
            settings.db_url
        )
    else:
        push_config_store = InMemoryPushNotificationConfigStore()
    push_sender = BasePushNotificationSender(
        httpx_client=httpx_client,
        config_store=push_config_store
    )
    # Configure the tasks store system
    if settings.use_db_task_store:
        task_store = DatabaseTaskStore(settings.db_url)
    else:
        task_store = InMemoryTaskStore()
    request_handler = DefaultRequestHandler(
        agent_executor=executor_instance,
        task_store=task_store,
        push_config_store=push_config_store,
        push_sender=push_sender
    )
    # Server configuration
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler
    )
    # Start the server
    uvicorn.run(
        server.build(),
        host=settings.a2a_host,
        port=settings.a2a_port
    )


# Run
def run():
    # logging
    setup_logging()
    logger.info("Starting server")
    main()


if __name__ == "__main__":
    run()