"""
Model Context Protocol (MCP) JSON-RPC 2.0 Server Interface
Provides standard MCP server protocol compliance to expose tools to any OSS LLM agent.
"""

import json
from typing import Dict, Any
from mcp_server.tools import MCPToolRegistry

class MCPServer:
    """Standard Model Context Protocol Server Interface."""

    def __init__(self, simulation_engine):
        self.registry = MCPToolRegistry(simulation_engine)

    def handle_json_rpc_request(self, json_rpc_payload: str) -> str:
        """Processes JSON-RPC 2.0 request from LLM agent client."""
        try:
            req = json.loads(json_rpc_payload)
            method = req.get("method")
            req_id = req.get("id", 1)

            if method == "tools/list":
                tools = self.registry.get_tool_definitions()
                return json.dumps({
                    "jsonrpc": "2.0",
                    "result": {"tools": tools},
                    "id": req_id
                })

            elif method == "tools/call":
                params = req.get("params", {})
                name = params.get("name")
                args = params.get("arguments", {})
                result = self.registry.execute_tool(name, args)
                return json.dumps({
                    "jsonrpc": "2.0",
                    "result": result,
                    "id": req_id
                })

            else:
                return json.dumps({
                    "jsonrpc": "2.0",
                    "error": {"code": -32601, "message": "Method not found"},
                    "id": req_id
                })

        except Exception as e:
            return json.dumps({
                "jsonrpc": "2.0",
                "error": {"code": -32603, "message": f"Internal RPC Error: {str(e)}"},
                "id": 1
            })
