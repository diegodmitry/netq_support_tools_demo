import { describe, expect, it } from "vitest";

import { decodeDisplayEntities } from "./code-viewer";
import {
  buildXmlNodeId,
  buildXmlErrorExcerpt,
  extractXmlErrorLocation,
  formatCollapsedXmlSummary,
  formatXmlAttributes,
  isExpandableXmlNode,
  parseXmlTree,
  type XmlTreeNode,
} from "./code-viewer-xml";

describe("decodeDisplayEntities", () => {
  it("decodes escaped xml brackets for display", () => {
    expect(decodeDisplayEntities("&lt;tag&gt;value&lt;/tag&gt;")).toBe(
      "<tag>value</tag>",
    );
  });

  it("decodes mixed xml entities without dropping content", () => {
    expect(
      decodeDisplayEntities("&lt;tag attr=&quot;1&quot;&gt;A&amp;B&lt;/tag&gt;"),
    ).toBe('<tag attr="1">A&B</tag>');
  });
});

describe("code viewer xml helpers", () => {
  it("formats xml attributes in source order", () => {
    expect(
      formatXmlAttributes([
        { name: "class", value: "linked-hash-map" },
        { name: "name", value: "partial" },
      ]),
    ).toBe('class="linked-hash-map" name="partial"');
  });

  it("formats a collapsed xml summary for expandable nodes", () => {
    expect(
      formatCollapsedXmlSummary("order", [{ name: "id", value: "123" }]),
    ).toBe('<order id="123">...</order>');
  });

  it("builds stable ids from path, index and label", () => {
    expect(buildXmlNodeId(["root", "0:order"], 2, "param")).toBe(
      "root/0:order/2:param",
    );
  });

  it("detects expandable xml element nodes", () => {
    const expandableNode: XmlTreeNode = {
      id: "root/0:order",
      type: "element",
      tagName: "order",
      attributes: [],
      textContent: null,
      children: [
        {
          id: "root/0:order/0:id",
          type: "element",
          tagName: "id",
          attributes: [],
          textContent: "123",
          children: [],
        },
      ],
    };

    const leafNode: XmlTreeNode = {
      id: "root/0:order/0:id",
      type: "element",
      tagName: "id",
      attributes: [],
      textContent: "123",
      children: [],
    };

    expect(isExpandableXmlNode(expandableNode)).toBe(true);
    expect(isExpandableXmlNode(leafNode)).toBe(false);
    expect(
      isExpandableXmlNode({
        id: "comment",
        type: "comment",
        content: "<!--note-->",
      }),
    ).toBe(false);
  });

  it("extracts line and column from DOMParser-style XML errors", () => {
    expect(
      extractXmlErrorLocation("error on line 18 at column 37: Opening and ending tag mismatch"),
    ).toEqual({
      line: 18,
      column: 37,
    });
  });

  it("builds a numbered excerpt around the XML parse failure", () => {
    expect(
      buildXmlErrorExcerpt("<root>\n  <child>\n  </root>", 2, 5),
    ).toBe(
      [
        "     1 | <root>",
        ">    2 |   <child>",
        "       |     ^",
        "     3 |   </root>",
      ].join("\n"),
    );
  });

  it.skipIf(typeof DOMParser === "undefined")(
    "parses xml that contains escaped ampersands in text content",
    () => {
    const parsed = parseXmlTree(
      '<?xml version="1.0" ?>\n<order>\n  <description>P&amp;S</description>\n</order>',
    );

    expect(parsed.parseError).toBe(false);
    expect(parsed.nodes).toHaveLength(1);
    },
  );
});
