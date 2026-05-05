import type { ReactNode } from "react";

import { classNames } from "@/shared/lib/classnames";

type Column<T> = {
  key: keyof T | string;
  header: ReactNode;
  align?: "left" | "right";
  render?: (row: T) => ReactNode;
};

type DataTableProps<T extends Record<string, ReactNode>> = {
  caption?: string;
  columns: Column<T>[];
  rows: T[];
  empty?: ReactNode;
  className?: string;
};

export function DataTable<T extends Record<string, ReactNode>>({
  caption,
  columns,
  rows,
  empty,
  className,
}: DataTableProps<T>) {
  if (rows.length === 0) {
    return <div className={classNames("table-empty", className)}>{empty}</div>;
  }

  return (
    <div className={classNames("table-shell", className)}>
      <table className="data-table">
        {caption ? <caption>{caption}</caption> : null}
        <thead>
          <tr>
            {columns.map((column) => (
              <th
                key={String(column.key)}
                className={column.align === "right" ? "align-right" : undefined}
                scope="col"
              >
                {column.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={String(row.id ?? index)}>
              {columns.map((column) => (
                <td
                  key={String(column.key)}
                  className={
                    column.align === "right" ? "align-right" : undefined
                  }
                >
                  {column.render
                    ? column.render(row)
                    : (row[column.key as keyof T] ?? "—")}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
