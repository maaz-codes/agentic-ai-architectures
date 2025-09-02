from langchain.callbacks.base import BaseCallbackHandler


class MyLogger(BaseCallbackHandler):
    def on_chain_start(self, serialized, inputs, *, run_id, parent_run_id = None, tags = None, metadata = None, **kwargs):
        print(f"Callback called chain_start: serialised{serialized} | inputs: {inputs}")

    
    def on_tool_start(self, serialized, input_str, *, run_id, parent_run_id = None, tags = None, metadata = None, inputs = None, **kwargs):
        print(f"Callback called tool_start: serialised{serialized} | input: {inputs}")
