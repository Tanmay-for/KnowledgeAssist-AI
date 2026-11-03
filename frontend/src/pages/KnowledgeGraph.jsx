import { useEffect, useState, useCallback } from "react";
import ForceGraph2D from "react-force-graph-2d";
import {
  Network,
  RefreshCw,
  GitBranch,
  CircleDot,
  ZoomIn,
  Info,
} from "lucide-react";

import { getKnowledgeGraph } from "../services/api";

function KnowledgeGraph() {
  const [graphData, setGraphData] = useState({
    nodes: [],
    links: [],
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [dimensions, setDimensions] = useState({
    width: 900,
    height: 520,
  });

  const [selectedNode, setSelectedNode] = useState(null);

  const loadGraph = useCallback(async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getKnowledgeGraph();

      setGraphData({
        nodes: (data.nodes || []).map((node) => ({
          ...node,
          id: node.id,
          label: node.label || node.id,
        })),

        links: (data.edges || []).map((edge) => ({
          source: edge.source,
          target: edge.target,
          relationship: edge.relationship || "related_to",
        })),
      });

      setSelectedNode(null);
    } catch (err) {
      setError(err.message || "Failed to load Knowledge Graph.");
    } finally {
      setLoading(false);
    }
  }, []);

  // Load graph when the page opens
  useEffect(() => {
    loadGraph();
  }, [loadGraph]);

  // Adjust graph width when browser window changes
  useEffect(() => {
    function updateDimensions() {
      const container = document.querySelector(".graph-visualization");

      if (container) {
        setDimensions({
          width: Math.max(300, container.clientWidth),
          height: window.innerWidth < 768 ? 450 : 560,
        });
      }
    }

    updateDimensions();

    window.addEventListener("resize", updateDimensions);

    return () => {
      window.removeEventListener("resize", updateDimensions);
    };
  }, [loading, error]);

  // Different colors for different concepts
  function getNodeColor(node) {
    const colors = {
      Class: "#8b7cff",
      Object: "#22c55e",
      Inheritance: "#f59e0b",
      Polymorphism: "#06b6d4",
      Encapsulation: "#ec4899",
      Abstraction: "#a78bfa",
      Constructor: "#14b8a6",
      Destructor: "#f97316",
      Function: "#3b82f6",
      "Data Member": "#e879f9",
      "Member Function": "#84cc16",
      "Object-Oriented Programming": "#facc15",
    };

    return colors[node.label] || "#8b7cff";
  }

  // Draw each concept node
  function drawNode(node, ctx, globalScale) {
    const label = node.label || node.id;
    const fontSize = Math.max(9, 13 / globalScale);
    const nodeSize = selectedNode?.id === node.id ? 9 : 7;

    ctx.beginPath();
    ctx.arc(node.x, node.y, nodeSize, 0, 2 * Math.PI);

    ctx.fillStyle = getNodeColor(node);
    ctx.fill();

    ctx.strokeStyle = selectedNode?.id === node.id ? "#ffffff" : "#c4b5fd";

    ctx.lineWidth = 1.5 / globalScale;
    ctx.stroke();

    ctx.font = `600 ${fontSize}px Sans-Serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "top";

    ctx.fillStyle = "#ffffff";
    ctx.fillText(label, node.x, node.y + nodeSize + 4);
  }

  return (
    <div className="graph-page">
      {/* Page Header */}
      <div className="graph-header">
        <div>
          <h1>Knowledge Graph</h1>
          <p>
            Explore concepts and their relationships in your uploaded documents.
          </p>
        </div>

        <button
          type="button"
          className="graph-refresh-btn"
          onClick={loadGraph}
          disabled={loading}
        >
          <RefreshCw size={17} className={loading ? "refresh-spinning" : ""} />
          Refresh
        </button>
      </div>

      {/* Graph Statistics */}
      <div className="graph-stats">
        <div className="graph-stat-card">
          <CircleDot size={23} />

          <div>
            <h2>{graphData.nodes.length}</h2>
            <p>Total Concepts</p>
          </div>
        </div>

        <div className="graph-stat-card">
          <GitBranch size={23} />

          <div>
            <h2>{graphData.links.length}</h2>
            <p>Relationships</p>
          </div>
        </div>

        <div className="graph-stat-card">
          <Network size={23} />

          <div>
            <h2>
              {
                graphData.nodes.filter((node) =>
                  graphData.links.some(
                    (link) =>
                      (typeof link.source === "object"
                        ? link.source.id
                        : link.source) === node.id ||
                      (typeof link.target === "object"
                        ? link.target.id
                        : link.target) === node.id
                  )
                ).length
              }
            </h2>
            <p>Connected Concepts</p>
          </div>
        </div>
      </div>

      {/* Graph Visualization */}
      <div className="graph-container">
        <div className="graph-title">
          <Network size={19} />
          <h3>Concept Relationship Map</h3>
        </div>

        {loading ? (
          <div className="graph-message">
            <RefreshCw size={25} className="refresh-spinning" />
            <p>Loading Knowledge Graph...</p>
          </div>
        ) : error ? (
          <div className="graph-error">{error}</div>
        ) : graphData.nodes.length === 0 ? (
          <div className="graph-message">
            <Network size={35} />
            <p>No concepts found. Upload a document first.</p>
          </div>
        ) : (
          <div className="graph-visualization">
            <ForceGraph2D
              graphData={graphData}
              width={dimensions.width}
              height={dimensions.height}
              backgroundColor="#101827"
              // Node settings
              nodeId="id"
              nodeLabel={(node) => node.label}
              nodeRelSize={7}
              nodeCanvasObject={drawNode}
              nodeCanvasObjectMode={() => "replace"}
              // Connection line settings
              linkWidth={2.5}
              linkColor={() => "#a78bfa"}
              linkOpacity={0.9}
              // Directional arrows
              linkDirectionalArrowLength={7}
              linkDirectionalArrowRelPos={1}
              linkDirectionalArrowColor={() => "#c4b5fd"}
              // Animated particles
              linkDirectionalParticles={2}
              linkDirectionalParticleWidth={3}
              linkDirectionalParticleSpeed={0.003}
              linkDirectionalParticleColor={() => "#ffffff"}
              // Relationship label on hover
              linkLabel={(link) => `${link.relationship || "related_to"}`}
              // Node selection
              onNodeClick={(node) => setSelectedNode(node)}
              // Force layout
              d3AlphaDecay={0.02}
              d3VelocityDecay={0.3}
              cooldownTicks={200}
              // Allow graph interaction
              enableNodeDrag={true}
              enableZoomInteraction={true}
              enablePanInteraction={true}
            />
          </div>
        )}
      </div>

      {/* Selected Concept Details */}
      {selectedNode && (
        <div className="selected-concept-card">
          <div>
            <h3>{selectedNode.label}</h3>
            <p>Concept Type: {selectedNode.type || "Concept"}</p>
          </div>

          <button type="button" onClick={() => setSelectedNode(null)}>
            Close
          </button>
        </div>
      )}

      {/* Graph Instructions */}
      <div className="graph-hint">
        <Info size={17} />

        <p>
          Drag concepts to move them. Scroll to zoom. Click a concept to view
          its details. Hover over a connection to see its relationship.
        </p>
      </div>

      {/* Legend */}
      <div className="graph-legend">
        <h3>Graph Legend</h3>

        <div className="legend-items">
          <span>
            <i style={{ background: "#8b7cff" }} />
            Class
          </span>

          <span>
            <i style={{ background: "#22c55e" }} />
            Object
          </span>

          <span>
            <i style={{ background: "#f59e0b" }} />
            Inheritance
          </span>

          <span>
            <i style={{ background: "#06b6d4" }} />
            Polymorphism
          </span>

          <span>
            <i style={{ background: "#ec4899" }} />
            Encapsulation
          </span>

          <span>
            <i style={{ background: "#a78bfa" }} />
            Abstraction
          </span>
        </div>
      </div>
    </div>
  );
}

export default KnowledgeGraph;
