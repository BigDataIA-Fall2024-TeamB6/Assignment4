"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  useCoAgent,
  useCoAgentStateRender,
  useCopilotAction,
} from "@copilotkit/react-core";
import { Progress } from "./Progress";
import { EditResourceDialog } from "./EditResourceDialog";
import { AddResourceDialog } from "./AddResourceDialog";
import { Resources } from "./Resources";
import { AgentState, Resource } from "@/lib/types";
import { useModelSelectorContext } from "@/lib/model-selector-provider";
import { useEffect } from "react";

export function ResearchCanvas() {
  const { model, agent } = useModelSelectorContext();

  const { state, setState } = useCoAgent<AgentState>({
    name: agent,
    initialState: {
      model,
    },
  });

  useCoAgentStateRender({
    name: agent,
    render: ({ state, nodeName, status }) => {
      if (!state.logs || state.logs.length === 0) {
        return null;
      }
      return <Progress logs={state.logs} />;
    },
  });

  useCopilotAction({
    name: "DeleteResources",
    disabled: true,
    parameters: [
      {
        name: "urls",
        type: "string[]",
      },
    ],
    renderAndWait: ({ args, status, handler }) => {
      return (
        <div className="">
          <div className="font-bold text-base mb-2">
            Delete these resources?
          </div>
          <Resources
            resources={resources.filter((resource) =>
              (args.urls || []).includes(resource.url)
            )}
            customWidth={200}
          />
          {status === "executing" && (
            <div className="mt-4 flex justify-start space-x-2">
              <button
                onClick={() => handler("NO")}
                className="px-4 py-2 text-[#6766FC] border border-[#6766FC] rounded text-sm font-bold"
              >
                Cancel
              </button>
              <button
                onClick={() => handler("YES")}
                className="px-4 py-2 bg-[#6766FC] text-white rounded text-sm font-bold"
              >
                Delete
              </button>
            </div>
          )}
        </div>
      );
    },
  });

  const resources: Resource[] = state.resources || [];
  const setResources = (resources: Resource[]) => {
    setState({ ...state, resources });
  };

  // const [resources, setResources] = useState<Resource[]>(dummyResources);
  const [newResource, setNewResource] = useState<Resource>({
    url: "",
    title: "",
    description: "",
  });
  const [isAddResourceOpen, setIsAddResourceOpen] = useState(false);

  const addResource = () => {
    if (newResource.url) {
      setResources([...resources, { ...newResource }]);
      setNewResource({ url: "", title: "", description: "" });
      setIsAddResourceOpen(false);
    }
  };

  const removeResource = (url: string) => {
    setResources(
      resources.filter((resource: Resource) => resource.url !== url)
    );
  };

  const [editResource, setEditResource] = useState<Resource | null>(null);
  const [originalUrl, setOriginalUrl] = useState<string | null>(null);
  const [isEditResourceOpen, setIsEditResourceOpen] = useState(false);

  const handleCardClick = (resource: Resource) => {
    setEditResource({ ...resource }); // Ensure a new object is created
    setOriginalUrl(resource.url); // Store the original URL
    setIsEditResourceOpen(true);
  };

  const updateResource = () => {
    if (editResource && originalUrl) {
      setResources(
        resources.map((resource) =>
          resource.url === originalUrl ? { ...editResource } : resource
        )
      );
      setEditResource(null);
      setOriginalUrl(null);
      setIsEditResourceOpen(false);
    }
  };

  const handleExportPDF = async () => {
    try {
      const response = await fetch("http://localhost:8000/exportPDF", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ report: state.report }), // Send the report data if needed
      });
  
      if (response.ok) {
        const blob = await response.blob(); 
        const url = window.URL.createObjectURL(blob); 
        const link = document.createElement("a"); 
        link.href = url;
        link.download = "output.pdf"; 
        link.click(); 
        window.URL.revokeObjectURL(url); 
      } else {
        console.log("Failed to export PDF");
      }
    } catch (error) {
      console.error("Error exporting PDF:", error);
    }
  };

  const handleExportCodelabs = async () => {
    try {
      // Send a POST request to trigger the Codelab export on the backend
      const response = await fetch("http://localhost:8000/exportCodelabs", {
        method: "POST"
      });
  
      if (response.ok) {
        console.log("Codelab export successful.");
  
        // Open localhost:9000 in a new tab to view the Codelab
        window.open("http://localhost:9000", "_blank");
      } else {
        console.log("Failed to export Codelab");
      }
    } catch (error) {
      console.error("Error exporting Codelab:", error);
    }
  };

  const documents = [
    { id: "68db7e4f057f494fb5b939ba258cefcd", name: "Revisiting-the-Equity-Risk-Premium" },
    { id: "97b6383e18bb48d1b7daceb27ad0a198", name: "beyond-active-and-passive" },
    { id: "52af53cc2f5e42558253aa572a55b78a", name: "risk_compilation_2018" },
  ];

  const [selectedDocument, setSelectedDocument] = useState<{ id: string, name: string }>({ id: "", name: "" });

  useEffect(() => {
    if (selectedDocument.id) {
      // Send both the document ID and name via POST request to the specified endpoint
      const sendDocumentData = async () => {
        try {
          const response = await fetch("http://localhost:8000/sourcedocument", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              documentId: selectedDocument.id,
              documentName: selectedDocument.name,
            }),
          });

          if (response.ok) {
            console.log(`Document ID ${selectedDocument.id} and Name ${selectedDocument.name} sent successfully.`);
          } else {
            console.log("Failed to send document data.");
          }
        } catch (error) {
          console.error("Error sending document data:", error);
        }
      };

      sendDocumentData();
    }
  }, [selectedDocument]);

  return (
    <div className="container w-full h-full p-10 bg-slate-50 overflow-auto">
      <div className="space-y-8">
        <div>
          <h2 className="text-lg font-medium mb-3 text-primary">Select a Source Document</h2>
          <select
            value={selectedDocument.id}
            onChange={(e) => {
              const selectedDoc = documents.find(doc => doc.id === e.target.value);
              if (selectedDoc) {
                setSelectedDocument({ id: selectedDoc.id, name: selectedDoc.name });
              }
            }}
            className="bg-background px-6 py-3 border-2 rounded-lg text-md font-light focus-visible:ring-0 placeholder:text-slate-400 w-full"
            aria-label="Select Document"
          >
            <option value="">Select a document</option>
            {documents.map((document) => (
              <option key={document.id} value={document.id}>
                {document.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <h2 className="text-lg font-medium mb-3 text-primary">
            What do you want to research about?
          </h2>
          <Input
            placeholder="Your research question"
            value={state.research_question || ""}
            onChange={(e) =>
              setState({ ...state, research_question: e.target.value })
            }
            aria-label="Research question"
            className="bg-background px-6 py-8 border-2 shadow-none rounded-lg text-md font-extralight focus-visible:ring-0 placeholder:text-slate-400"
          />
        </div>

        <div>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-medium text-primary">Resources</h2>
            <EditResourceDialog
              isOpen={isEditResourceOpen}
              onOpenChange={setIsEditResourceOpen}
              editResource={editResource}
              setEditResource={setEditResource}
              updateResource={updateResource}
            />
            <AddResourceDialog
              isOpen={isAddResourceOpen}
              onOpenChange={setIsAddResourceOpen}
              newResource={newResource}
              setNewResource={setNewResource}
              addResource={addResource}
            />
          </div>
          {resources.length === 0 && (
            <div className="text-sm text-slate-400">
              Click the button above to add resources manually.
            </div>
          )}

          {resources.length !== 0 && (
            <Resources
              resources={resources}
              handleCardClick={handleCardClick}
              removeResource={removeResource}
            />
          )}
        </div>

        <div className="flex flex-col h-full">
          <h2 className="text-lg font-medium mb-3 text-primary">
            Research Draft
          </h2>
          <Textarea
            placeholder="Your research draft will be prepared here..."
            value={state.report || ""}
            onChange={(e) => setState({ ...state, report: e.target.value })}
            rows={10}
            aria-label="Research draft"
            className="bg-background px-6 py-8 border-2 shadow-none rounded-lg text-md font-extralight focus-visible:ring-0 placeholder:text-slate-400"
            style={{ minHeight: "500px" }}
          />
        </div>

        <div className="flex justify-end mt-8">
          
          {/* Export to PDF */}
          <button
            onClick={handleExportPDF}
            className="px-6 py-2 bg-[#6766FC] text-white rounded text-sm font-bold mr-3"
          >
            Export as PDF
          </button>

          {/* Export to Codelabs */}
          <button
            onClick={handleExportCodelabs}
            className="px-6 py-2 bg-[#6766FC] text-white rounded text-sm font-bold"
          >
            Export to Codelabs
          </button>
        </div>
      </div>
    </div>
  );
}
