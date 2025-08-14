# src\core\langraph_config.py
from contextlib import contextmanager
from langgraph.graph import StateGraph
from src.types_ import ConversationState
from src.core.langraph_checkpoint import open_langraph_sqlite, close_langraph_sqlite
from src.config.settings import settings


class LangGraphManager:
    def __init__(self, db_path: str = None):
        self.db_path = settings.LANGRAPH_DB_PATH
        self._conn = None
        self._checkpointer = None

    @contextmanager
    def get_app(self):

        try:
            self._conn, self._checkpointer = open_langraph_sqlite(self.db_path)
            workflow = self._build_workflow()
            app = workflow.compile(checkpointer=self._checkpointer)
            yield app
        finally:
            if self._conn:
                close_langraph_sqlite(self._conn)

    def _build_workflow(self) -> StateGraph:

        workflow = StateGraph(ConversationState)
        workflow.add_node("initialize", self._initialize_conversation)
        workflow.set_entry_point("initialize")
        workflow.set_finish_point("initialize")
        return workflow

    def _initialize_conversation(self, state: ConversationState):

        if not state.get("messages"):
            state["messages"] = []
            state["context"] = {}
        return state


# Usage:
# manager = LangGraphManager()
# with manager.get_app() as app:
#     # Use app here
#     pass
