from typing import TypedDict
import xml.etree.ElementTree as ET
from langgraph.graph import StateGraph, START, END

XML_FILE = "sample_kcash_credit_trans.xml"

class State(TypedDict):
    xml_text: str
    fileid: str
    operid: str
    amount: float

def load_xml(state: State):
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    ns = {"ns": "http://bpc.ru/sv/xp/clearing"}

    fileid = root.findtext("ns:fileid", namespaces=ns)
    operid = root.findtext("ns:operation/ns:operid", namespaces=ns)
    amount = root.findtext("ns:operation/ns:operamount/ns:amountvalue", namespaces=ns)

    return {
        "xml_text": state["xml_text"],
        "fileid": fileid,
        "operid": operid,
        "amount": amount,
    }

builder = StateGraph(State)
builder.add_node("load_xml", load_xml)
builder.add_edge(START, "load_xml")
builder.add_edge("load_xml", END)

graph = builder.compile()
result = graph.invoke({"xml_text": ""})
print(result)
