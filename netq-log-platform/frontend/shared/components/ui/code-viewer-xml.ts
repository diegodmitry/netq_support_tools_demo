export type XmlAttribute = {
  name: string;
  value: string;
};

export type XmlTreeNode =
  | {
      id: string;
      type: "declaration";
      content: string;
    }
  | {
      id: string;
      type: "comment";
      content: string;
    }
  | {
      id: string;
      type: "element";
      tagName: string;
      attributes: XmlAttribute[];
      textContent: string | null;
      children: XmlTreeNode[];
    };

export type ParsedXmlTree = {
  declaration: string | null;
  nodes: XmlTreeNode[];
  parseError: boolean;
  parseErrorMessage: string | null;
  parseErrorDiagnostic: XmlParseDiagnostic | null;
};

export type XmlParseDiagnostic = {
  line: number | null;
  column: number | null;
  excerpt: string | null;
  sourceText: string | null;
};

function normalizeTextContent(value: string) {
  const normalized = value.replace(/\s+/g, " ").trim();
  return normalized.length > 0 ? normalized : null;
}

export function buildXmlNodeId(path: string[], index: number, label: string) {
  return [...path, `${index}:${label}`].join("/");
}

export function formatXmlAttributes(attributes: XmlAttribute[]) {
  return attributes
    .map((attribute) => `${attribute.name}="${attribute.value}"`)
    .join(" ");
}

export function formatCollapsedXmlSummary(
  tagName: string,
  attributes: XmlAttribute[],
) {
  const serializedAttributes = formatXmlAttributes(attributes);
  const suffix = serializedAttributes.length > 0 ? ` ${serializedAttributes}` : "";

  return `<${tagName}${suffix}>...</${tagName}>`;
}

export function isExpandableXmlNode(node: XmlTreeNode) {
  return node.type === "element" && node.children.length > 0;
}

export function extractXmlErrorLocation(message: string) {
  const patterns = [
    /line\s+(\d+)\s+at\s+column\s+(\d+)/i,
    /line\s+(\d+),\s*column\s+(\d+)/i,
    /on line\s+(\d+)\s+at column\s+(\d+)/i,
    /line number\s+(\d+),\s*column\s+(\d+)/i,
  ];

  for (const pattern of patterns) {
    const match = message.match(pattern);
    if (match) {
      return {
        line: Number.parseInt(match[1] ?? "", 10),
        column: Number.parseInt(match[2] ?? "", 10),
      };
    }
  }

  return {
    line: null,
    column: null,
  };
}

export function buildXmlErrorExcerpt(
  code: string,
  line: number | null,
  column: number | null,
  radius = 2,
) {
  if (!line || line < 1) {
    return null;
  }

  const lines = code.replaceAll("\r\n", "\n").split("\n");
  const targetIndex = line - 1;
  if (targetIndex >= lines.length) {
    return null;
  }

  const start = Math.max(0, targetIndex - radius);
  const end = Math.min(lines.length - 1, targetIndex + radius);
  const formattedLines: string[] = [];

  for (let index = start; index <= end; index += 1) {
    const lineNumber = String(index + 1).padStart(4, " ");
    const marker = index === targetIndex ? ">" : " ";
    formattedLines.push(`${marker} ${lineNumber} | ${lines[index]}`);

    if (index === targetIndex && column && column > 0) {
      const pointerPadding = Math.max(column - 1, 0);
      formattedLines.push(`  ${" ".repeat(lineNumber.length)} | ${" ".repeat(pointerPadding)}^`);
    }
  }

  return formattedLines.join("\n");
}

function inferErrorLineFromSourceText(code: string, sourceText: string | null) {
  if (!sourceText) {
    return null;
  }

  const normalizedSourceText = sourceText.trim();
  if (normalizedSourceText.length === 0) {
    return null;
  }

  const lines = code.replaceAll("\r\n", "\n").split("\n");
  const matchedIndex = lines.findIndex((line) => line.includes(normalizedSourceText));
  return matchedIndex >= 0 ? matchedIndex + 1 : null;
}

function buildXmlParseDiagnostic(
  code: string,
  parseErrorMessage: string,
  parserError: Element,
): XmlParseDiagnostic {
  const sourceText = parserError.querySelector("sourcetext")?.textContent?.trim() ?? null;
  const location = extractXmlErrorLocation(parseErrorMessage);
  const inferredLine = inferErrorLineFromSourceText(code, sourceText);
  const line = location.line ?? inferredLine;
  const column = location.line ? location.column : null;

  return {
    line,
    column,
    excerpt: buildXmlErrorExcerpt(code, line, column),
    sourceText,
  };
}

function parseXmlNode(
  node: Node,
  path: string[],
  index: number,
): XmlTreeNode | null {
  if (node.nodeType === node.COMMENT_NODE) {
    const content = node.textContent?.trim() ?? "";
    if (content.length === 0) {
      return null;
    }

    return {
      id: buildXmlNodeId(path, index, "comment"),
      type: "comment",
      content: `<!--${content}-->`,
    };
  }

  if (node.nodeType !== node.ELEMENT_NODE) {
    return null;
  }

  const element = node as Element;
  const nodeId = buildXmlNodeId(path, index, element.tagName);
  const attributes = Array.from(element.attributes).map((attribute) => ({
    name: attribute.name,
    value: attribute.value,
  }));
  const children: XmlTreeNode[] = [];
  const textSegments: string[] = [];

  Array.from(element.childNodes).forEach((childNode, childIndex) => {
    if (childNode.nodeType === childNode.TEXT_NODE) {
      const normalized = normalizeTextContent(childNode.textContent ?? "");
      if (normalized) {
        textSegments.push(normalized);
      }
      return;
    }

    const parsedChild = parseXmlNode(childNode, [...path, `${index}:${element.tagName}`], childIndex);
    if (parsedChild) {
      children.push(parsedChild);
    }
  });

  return {
    id: nodeId,
    type: "element",
    tagName: element.tagName,
    attributes,
    textContent: textSegments.length > 0 ? textSegments.join(" ") : null,
    children,
  };
}

export function parseXmlTree(code: string): ParsedXmlTree {
  if (typeof DOMParser === "undefined") {
    return {
      declaration: null,
      nodes: [],
      parseError: true,
      parseErrorMessage: "DOMParser is not available in this runtime.",
      parseErrorDiagnostic: null,
    };
  }

  const declarationMatch = code.match(/^\s*(<\?xml[\s\S]*?\?>)/);
  const declaration = declarationMatch?.[1] ?? null;
  const parser = new DOMParser();
  const documentNode = parser.parseFromString(code, "application/xml");
  const parserError = documentNode.getElementsByTagName("parsererror")[0];

  if (parserError) {
    const parseErrorMessage = parserError.textContent?.trim() ?? "Invalid XML payload.";

    return {
      declaration,
      nodes: [],
      parseError: true,
      parseErrorMessage,
      parseErrorDiagnostic: buildXmlParseDiagnostic(code, parseErrorMessage, parserError),
    };
  }

  const nodes = Array.from(documentNode.childNodes)
    .map((node, index) => parseXmlNode(node, ["root"], index))
    .filter((node): node is XmlTreeNode => node !== null);

  return {
    declaration,
    nodes,
    parseError: false,
    parseErrorMessage: null,
    parseErrorDiagnostic: null,
  };
}
