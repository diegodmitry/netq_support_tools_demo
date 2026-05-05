"use client";

import { useState } from "react";

import { CodeViewer } from "@/shared/components/ui";

type PayloadView = {
  contentType: string;
  formatted: string;
  raw: string;
};

type NetqRecord = {
  orderId: string;
  orderType: string;
  auditPayload: PayloadView;
  mongoPayload: PayloadView;
  relatedOrderIds: string[];
};

type NetqPanel = "left" | "right";

function rowTitle(record: NetqRecord, panel: NetqPanel) {
  if (panel === "left") {
    return `Registo do pedido com o ID: ${record.orderId} - ${record.orderType}`;
  }

  return `Pedidos a sistemas externos relacionado com o ID: ${record.orderId} - ${record.orderType}`;
}

function buildColumnCopy(records: NetqRecord[], panel: NetqPanel) {
  return records
    .map((record) => {
      const payload =
        panel === "left" ? record.mongoPayload.formatted : record.auditPayload.formatted;

      return [rowTitle(record, panel), payload].join("\n\n");
    })
    .join("\n\n----------------------------------------\n\n");
}

function NetqAccordionColumn({
  title,
  panel,
  records,
  expandedOrderId,
  onToggle,
  onCopyAll,
  copied,
}: {
  title: string;
  panel: NetqPanel;
  records: NetqRecord[];
  expandedOrderId: string | null;
  onToggle: (orderId: string) => void;
  onCopyAll: (panel: NetqPanel) => void;
  copied: boolean;
}) {
  return (
    <section className="netq-column">
      <header className="netq-column-header">
        <strong>{title}</strong>
        <button
          type="button"
          className="button-secondary netq-column-copy-button"
          onClick={() => onCopyAll(panel)}
        >
          {copied ? "Copied" : "Copy all"}
        </button>
      </header>

      <div className="netq-accordion-list">
        {records.map((record) => {
          const expanded = expandedOrderId === record.orderId;
          const payload =
            panel === "left" ? record.mongoPayload.formatted : record.auditPayload.formatted;

          return (
            <article key={`${panel}:${record.orderId}`} className="netq-accordion-item">
              <button
                type="button"
                className={`netq-accordion-trigger${expanded ? " is-expanded" : ""}`}
                onClick={() => onToggle(record.orderId)}
                aria-expanded={expanded}
              >
                <span className="netq-accordion-title">{rowTitle(record, panel)}</span>
                <span className="netq-accordion-symbol" aria-hidden="true">
                  {expanded ? "-" : "+"}
                </span>
              </button>

              {expanded ? (
                <div className="netq-accordion-content">
                  <CodeViewer
                    title={panel === "left" ? "Request record" : "External systems"}
                    code={payload}
                    language="xml"
                    meta={
                      panel === "left"
                        ? "Legacy left panel: mongo/order payload"
                        : "Legacy right panel: audit/external systems payload"
                    }
                  />
                </div>
              ) : null}
            </article>
          );
        })}
      </div>
    </section>
  );
}

export function NetqResults({
  environment: _environment,
  records,
}: {
  environment: "prod" | "qa";
  records: NetqRecord[];
}) {
  const rootRecord = records[0] ?? null;
  const [expandedLeftOrderId, setExpandedLeftOrderId] = useState<string | null>(null);
  const [expandedRightOrderId, setExpandedRightOrderId] = useState<string | null>(null);
  const [copiedPanel, setCopiedPanel] = useState<NetqPanel | null>(null);

  function toggleLeft(orderId: string) {
    setExpandedLeftOrderId((current) => (current === orderId ? null : orderId));
  }

  function toggleRight(orderId: string) {
    setExpandedRightOrderId((current) => (current === orderId ? null : orderId));
  }

  async function copyAll(panel: NetqPanel) {
    const text = buildColumnCopy(records, panel);
    await navigator.clipboard.writeText(text);
    setCopiedPanel(panel);
    window.setTimeout(() => {
      setCopiedPanel((current) => (current === panel ? null : current));
    }, 1800);
  }

  return (
    <div className="stack netq-results netq-results-expanded">
      <section className="netq-summary-card">
        <span className="netq-summary-icon" aria-hidden="true">
          i
        </span>
        <div className="netq-summary-text">
          <p>
            {rootRecord
              ? `${rootRecord.orderId} · ${rootRecord.orderType}`
              : "NETQ result"}
          </p>
          <span>{records.length} records returned.</span>
        </div>
      </section>

      <section className="netq-legacy-grid">
        <NetqAccordionColumn
          title="Orders"
          panel="left"
          records={records}
          expandedOrderId={expandedLeftOrderId}
          onToggle={toggleLeft}
          onCopyAll={copyAll}
          copied={copiedPanel === "left"}
        />

        <NetqAccordionColumn
          title="External systems"
          panel="right"
          records={records}
          expandedOrderId={expandedRightOrderId}
          onToggle={toggleRight}
          onCopyAll={copyAll}
          copied={copiedPanel === "right"}
        />
      </section>
    </div>
  );
}
