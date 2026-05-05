"use client";

import { useEffect, useRef, useState, type CSSProperties, type ReactNode } from "react";

import { classNames } from "@/shared/lib/classnames";
import { Button } from "./button";
import {
  formatCollapsedXmlSummary,
  formatXmlAttributes,
  isExpandableXmlNode,
  parseXmlTree,
  type XmlAttribute,
  type XmlTreeNode,
} from "./code-viewer-xml";

type CodeViewerProps = {
  title: string;
  code: string;
  language?: string;
  meta?: ReactNode;
  actions?: ReactNode;
  className?: string;
  defaultExpanded?: boolean;
};

const XML_ENTITY_MAP: Record<string, string> = {
  "&lt;": "<",
  "&gt;": ">",
  "&amp;": "&",
  "&quot;": '"',
  "&#39;": "'",
};

export function decodeDisplayEntities(value: string) {
  return value.replaceAll(
    /&(lt|gt|amp|quot|#39);/g,
    (entity) => XML_ENTITY_MAP[entity] ?? entity,
  );
}

function escapeHtml(value: string) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function highlightXml(code: string) {
  const escaped = escapeHtml(decodeDisplayEntities(code));

  return escaped.replace(
    /(&lt;!--[\s\S]*?--&gt;)|(&lt;\?[\s\S]*?\?&gt;)|(&lt;\/?)([\w:.-]+)([\s\S]*?)(\/?&gt;)/g,
    (match, comment, processing, open, tagName, attributes = "", close) => {
      if (comment) {
        return `<span class="token token-comment">${comment}</span>`;
      }

      if (processing) {
        return `<span class="token token-processing">${processing}</span>`;
      }

      const highlightedAttributes = attributes.replace(
        /([\w:.-]+)(=)(&quot;.*?&quot;)/g,
        '<span class="token token-attr-name">$1</span><span class="token token-punctuation">$2</span><span class="token token-attr-value">$3</span>',
      );

      return [
        `<span class="token token-punctuation">${open}</span>`,
        `<span class="token token-tag">${tagName}</span>`,
        highlightedAttributes,
        `<span class="token token-punctuation">${close}</span>`,
      ].join("");
    },
  );
}

function highlightCode(code: string, language: string) {
  if (language === "xml") {
    return highlightXml(code);
  }

  return escapeHtml(decodeDisplayEntities(code));
}

function XmlAttributeList({ attributes }: { attributes: XmlAttribute[] }) {
  if (attributes.length === 0) {
    return null;
  }

  return (
    <>
      {" "}
      {attributes.map((attribute, index) => (
        <span key={`${attribute.name}:${attribute.value}`}>
          <span className="token token-attr-name">{attribute.name}</span>
          <span className="token token-punctuation">=</span>
          <span className="token token-attr-value">&quot;{attribute.value}&quot;</span>
          {index < attributes.length - 1 ? " " : null}
        </span>
      ))}
    </>
  );
}

function XmlOpenTag({
  tagName,
  attributes,
}: {
  tagName: string;
  attributes: XmlAttribute[];
}) {
  return (
    <>
      <span className="token token-punctuation">&lt;</span>
      <span className="token token-tag">{tagName}</span>
      <XmlAttributeList attributes={attributes} />
      <span className="token token-punctuation">&gt;</span>
    </>
  );
}

function XmlCloseTag({ tagName }: { tagName: string }) {
  return (
    <>
      <span className="token token-punctuation">&lt;/</span>
      <span className="token token-tag">{tagName}</span>
      <span className="token token-punctuation">&gt;</span>
    </>
  );
}

function XmlCollapsedSummary({
  tagName,
  attributes,
}: {
  tagName: string;
  attributes: XmlAttribute[];
}) {
  const summary = formatCollapsedXmlSummary(tagName, attributes);
  const serializedAttributes = formatXmlAttributes(attributes);
  const hasAttributes = serializedAttributes.length > 0;

  return (
    <>
      <span className="token token-punctuation">&lt;</span>
      <span className="token token-tag">{tagName}</span>
      {hasAttributes ? (
        <>
          {" "}
          {attributes.map((attribute, index) => (
            <span key={`${attribute.name}:${attribute.value}`}>
              <span className="token token-attr-name">{attribute.name}</span>
              <span className="token token-punctuation">=</span>
              <span className="token token-attr-value">&quot;{attribute.value}&quot;</span>
              {index < attributes.length - 1 ? " " : null}
            </span>
          ))}
        </>
      ) : null}
      <span className="token token-punctuation">&gt;</span>
      <span className="code-tree-collapsed-marker">...</span>
      <span className="token token-punctuation">&lt;/</span>
      <span className="token token-tag">{tagName}</span>
      <span className="token token-punctuation">&gt;</span>
      <span className="code-tree-screenreader">{summary}</span>
    </>
  );
}

function collectExpandableNodeIds(nodes: XmlTreeNode[], ids: string[] = []) {
  nodes.forEach((node) => {
    if (node.type === "element" && isExpandableXmlNode(node)) {
      ids.push(node.id);
      collectExpandableNodeIds(node.children, ids);
    }
  });

  return ids;
}

function XmlCodeTree({
  parsedXmlTree,
  defaultExpanded,
}: {
  parsedXmlTree: ReturnType<typeof parseXmlTree>;
  defaultExpanded: boolean;
}) {
  const [expandedNodeIds, setExpandedNodeIds] = useState<Set<string>>(
    () =>
      new Set(
        defaultExpanded ? collectExpandableNodeIds(parsedXmlTree.nodes) : [],
      ),
  );
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  function toggleNode(nodeId: string) {
    setExpandedNodeIds((current) => {
      const next = new Set(current);

      if (next.has(nodeId)) {
        next.delete(nodeId);
      } else {
        next.add(nodeId);
      }

      return next;
    });
  }

  return (
    <code data-language="xml" className="code-tree">
      {parsedXmlTree.declaration ? (
        <XmlTreeNodeRow
          node={{
            id: "xml-declaration",
            type: "declaration",
            content: parsedXmlTree.declaration,
          }}
          depth={0}
          expandedNodeIds={expandedNodeIds}
          selectedNodeId={selectedNodeId}
          onToggle={toggleNode}
          onSelect={setSelectedNodeId}
        />
      ) : null}
      {parsedXmlTree.nodes.map((node) => (
        <XmlTreeNodeRow
          key={node.id}
          node={node}
          depth={0}
          expandedNodeIds={expandedNodeIds}
          selectedNodeId={selectedNodeId}
          onToggle={toggleNode}
          onSelect={setSelectedNodeId}
        />
      ))}
    </code>
  );
}

function XmlTreeNodeRow({
  node,
  depth,
  expandedNodeIds,
  selectedNodeId,
  onToggle,
  onSelect,
}: {
  node: XmlTreeNode;
  depth: number;
  expandedNodeIds: Set<string>;
  selectedNodeId: string | null;
  onToggle: (nodeId: string) => void;
  onSelect: (nodeId: string) => void;
}) {
  if (node.type === "declaration") {
    return (
      <div className="code-tree-line" style={{ "--tree-depth": depth } as CSSProperties}>
        <div className="code-tree-line-content">
          <span className="token token-processing">{node.content}</span>
        </div>
      </div>
    );
  }

  if (node.type === "comment") {
    return (
      <div className="code-tree-line" style={{ "--tree-depth": depth } as CSSProperties}>
        <div className="code-tree-line-content">
          <span className="token token-comment">{node.content}</span>
        </div>
      </div>
    );
  }

  const expandable = isExpandableXmlNode(node);
  const expanded = expandable ? expandedNodeIds.has(node.id) : false;
  const selected = selectedNodeId === node.id;
  const hasTextContent = (node.textContent?.length ?? 0) > 0;
  const isLeaf = node.children.length === 0;

  if (!expandable) {
    return (
      <div
        className={classNames("code-tree-node", selected && "is-selected")}
        style={{ "--tree-depth": depth } as CSSProperties}
      >
        <div
          className={classNames("code-tree-line", selected && "is-selected")}
          style={{ "--tree-depth": depth } as CSSProperties}
        >
          <button
            type="button"
            className="code-tree-node-button"
            onClick={() => onSelect(node.id)}
          >
            <span className="code-tree-chevron-spacer" aria-hidden="true" />
            <span className="code-tree-line-content">
              <XmlOpenTag tagName={node.tagName} attributes={node.attributes} />
              {hasTextContent ? (
                <>
                  <span className="code-tree-text">{node.textContent}</span>
                  <XmlCloseTag tagName={node.tagName} />
                </>
              ) : (
                <>
                  <span className="token token-punctuation">&gt;&lt;/</span>
                  <span className="token token-tag">{node.tagName}</span>
                  <span className="token token-punctuation">&gt;</span>
                </>
              )}
            </span>
          </button>
        </div>
      </div>
    );
  }

  return (
    <div
      className={classNames("code-tree-node", selected && "is-selected")}
      style={{ "--tree-depth": depth } as CSSProperties}
    >
      <div
        className={classNames("code-tree-line", selected && "is-selected")}
        style={{ "--tree-depth": depth } as CSSProperties}
      >
        <button
          type="button"
          className="code-tree-chevron-button"
          onClick={() => {
            onSelect(node.id);
            onToggle(node.id);
          }}
          aria-expanded={expanded}
          aria-label={expanded ? `Collapse ${node.tagName}` : `Expand ${node.tagName}`}
        >
          {expanded ? "⌄" : "›"}
        </button>
        <button
          type="button"
          className="code-tree-node-button"
          onClick={() => onSelect(node.id)}
        >
          <span className="code-tree-line-content">
            {expanded ? (
              <XmlOpenTag tagName={node.tagName} attributes={node.attributes} />
            ) : (
              <XmlCollapsedSummary tagName={node.tagName} attributes={node.attributes} />
            )}
          </span>
        </button>
      </div>

      {expanded ? (
        <>
          {hasTextContent ? (
            <div className="code-tree-line" style={{ "--tree-depth": depth + 1 } as CSSProperties}>
              <div className="code-tree-line-content code-tree-text">{node.textContent}</div>
            </div>
          ) : null}
          {node.children.map((childNode) => (
            <XmlTreeNodeRow
              key={childNode.id}
              node={childNode}
              depth={depth + 1}
              expandedNodeIds={expandedNodeIds}
              selectedNodeId={selectedNodeId}
              onToggle={onToggle}
              onSelect={onSelect}
            />
          ))}
          {!isLeaf ? (
            <div className="code-tree-line" style={{ "--tree-depth": depth } as CSSProperties}>
              <div className="code-tree-line-content">
                <span className="code-tree-chevron-spacer" aria-hidden="true" />
                <XmlCloseTag tagName={node.tagName} />
              </div>
            </div>
          ) : null}
        </>
      ) : null}
    </div>
  );
}

export function CodeViewer({
  title,
  code,
  language = "text",
  meta,
  actions,
  className,
  defaultExpanded = true,
}: CodeViewerProps) {
  const minZoomLevel = -2;
  const maxZoomLevel = 2;
  const [copied, setCopied] = useState(false);
  const [zoomLevel, setZoomLevel] = useState(0);
  const [hasHorizontalOverflow, setHasHorizontalOverflow] = useState(false);
  const [scrollContentWidth, setScrollContentWidth] = useState(0);
  const scrollContainerRef = useRef<HTMLDivElement | null>(null);
  const scrollRailRef = useRef<HTMLDivElement | null>(null);
  const syncingScrollRef = useRef<"content" | "rail" | null>(null);
  const highlightedCode = highlightCode(code, language);
  const parsedXmlTree = language === "xml" ? parseXmlTree(code) : null;

  useEffect(() => {
    if (language !== "xml" || !parsedXmlTree?.parseError) {
      return;
    }

    const diagnosticSummary = parsedXmlTree.parseErrorDiagnostic
      ? {
          line: parsedXmlTree.parseErrorDiagnostic.line,
          column: parsedXmlTree.parseErrorDiagnostic.column,
          sourceText: parsedXmlTree.parseErrorDiagnostic.sourceText,
          excerpt: parsedXmlTree.parseErrorDiagnostic.excerpt,
        }
      : null;

    console.warn("CodeViewer XML tree fallback: invalid XML payload.", {
      title,
      parseErrorMessage: parsedXmlTree.parseErrorMessage,
      diagnostic: diagnosticSummary,
      preview: code.slice(0, 600),
    });
  }, [code, language, parsedXmlTree, title]);

  useEffect(() => {
    if (!scrollContainerRef.current) {
      return;
    }

    function updateMeasurements() {
      const container = scrollContainerRef.current;
      if (!container) {
        return;
      }

      setHasHorizontalOverflow(container.scrollWidth > container.clientWidth + 1);
      setScrollContentWidth(container.scrollWidth);
    }

    updateMeasurements();

    const observer = new ResizeObserver(() => {
      updateMeasurements();
    });
    observer.observe(scrollContainerRef.current);

    window.addEventListener("resize", updateMeasurements);

    return () => {
      observer.disconnect();
      window.removeEventListener("resize", updateMeasurements);
    };
  }, [code, zoomLevel]);

  async function handleCopy() {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
  }

  function zoomOut() {
    setZoomLevel((current) => Math.max(current - 1, minZoomLevel));
  }

  function zoomIn() {
    setZoomLevel((current) => Math.min(current + 1, maxZoomLevel));
  }

  function syncFromContent() {
    if (syncingScrollRef.current === "rail") {
      syncingScrollRef.current = null;
      return;
    }

    const container = scrollContainerRef.current;
    const rail = scrollRailRef.current;
    if (!container || !rail) {
      return;
    }

    syncingScrollRef.current = "content";
    rail.scrollLeft = container.scrollLeft;
  }

  function syncFromRail() {
    if (syncingScrollRef.current === "content") {
      syncingScrollRef.current = null;
      return;
    }

    const container = scrollContainerRef.current;
    const rail = scrollRailRef.current;
    if (!container || !rail) {
      return;
    }

    syncingScrollRef.current = "rail";
    container.scrollLeft = rail.scrollLeft;
  }

  return (
    <section className={classNames("code-viewer", className)}>
      <div className="code-viewer-header">
        <div className="code-viewer-copy">
          <strong>{title}</strong>
          {meta ? <div className="code-viewer-meta">{meta}</div> : null}
        </div>
        <div className="code-viewer-actions">
          <Button
            type="button"
            variant="secondary"
            className="code-viewer-action-button"
            onClick={zoomOut}
            disabled={zoomLevel <= minZoomLevel}
            title="Decrease zoom"
          >
            A-
          </Button>
          <Button
            type="button"
            variant="secondary"
            className="code-viewer-action-button"
            onClick={zoomIn}
            disabled={zoomLevel >= maxZoomLevel}
            title="Increase zoom"
          >
            A+
          </Button>
          <Button
            type="button"
            variant="secondary"
            className="code-viewer-action-button"
            onClick={() => void handleCopy()}
            title="Copy code"
          >
            {copied ? "Copied" : "Copy"}
          </Button>
          {actions}
        </div>
      </div>
      <div
        ref={scrollContainerRef}
        className="code-block-scroll"
        onScroll={syncFromContent}
      >
        {language === "xml" && parsedXmlTree?.parseError ? (
          <div className="code-viewer-warning" role="note">
            Tree view unavailable for this payload. Check the browser console for the XML parse error.
            {parsedXmlTree.parseErrorDiagnostic?.line ? (
              <>{" "}Line {parsedXmlTree.parseErrorDiagnostic.line}</>
            ) : null}
            {parsedXmlTree.parseErrorDiagnostic?.column ? (
              <>, column {parsedXmlTree.parseErrorDiagnostic.column}</>
            ) : null}
            .
          </div>
        ) : null}
        <pre
          className={classNames(
            "code-block",
            language === "xml" &&
              parsedXmlTree &&
              !parsedXmlTree.parseError &&
              "code-block-tree",
            zoomLevel === -2 && "code-block-xcompact",
            zoomLevel === -1 && "code-block-compact",
            zoomLevel === 1 && "code-block-large",
            zoomLevel === 2 && "code-block-xlarge",
          )}
        >
          {language === "xml" && parsedXmlTree && !parsedXmlTree.parseError ? (
            <XmlCodeTree
              key={`${language}:${code}`}
              parsedXmlTree={parsedXmlTree}
              defaultExpanded={defaultExpanded}
            />
          ) : (
            <code
              data-language={language}
              dangerouslySetInnerHTML={{ __html: highlightedCode }}
            />
          )}
        </pre>
      </div>
      {hasHorizontalOverflow ? (
        <div
          ref={scrollRailRef}
          className="code-block-scroll-rail"
          onScroll={syncFromRail}
          aria-hidden="true"
        >
          <div
            className="code-block-scroll-rail-content"
            style={{ width: `${scrollContentWidth}px` }}
          />
        </div>
      ) : null}
    </section>
  );
}
