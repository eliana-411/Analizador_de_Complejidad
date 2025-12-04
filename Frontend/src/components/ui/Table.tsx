import { For, Show } from 'solid-js';
import type { JSX } from 'solid-js';
import { ChevronDown } from 'lucide-solid';

export interface Column<T> {
  key: keyof T | string;
  header: string;
  width?: string;
  render?: (item: T, index: number) => JSX.Element;
}

export interface TableProps<T> {
  data: T[];
  columns: Column<T>[];
  expandable?: boolean;
  expandedContent?: (item: T, index: number) => JSX.Element;
  expandedRows?: Set<number>;
  onRowClick?: (item: T, index: number) => void;
  class?: string;
}

/**
 * Reusable table component with glass-morphism styling
 * Supports expandable rows with smooth animations
 */
export default function Table<T extends Record<string, any>>(props: TableProps<T>) {
  const isRowExpanded = (index: number) => props.expandedRows?.has(index) || false;

  const getCellValue = (item: T, key: string): any => {
    return item[key as keyof T];
  };

  return (
    <div class={`glass border-2 border-gray-300 rounded-lg overflow-hidden elevation-2 ${props.class || ''}`}>
      {/* Table Header */}
      <div class="bg-white/20 border-b-2 border-gray-300">
        <div class="flex items-center">
          <For each={props.columns}>
            {(column) => (
              <div
                class={`px-4 py-3 font-semibold text-gray-900 text-sm ${column.width || 'flex-1'}`}
              >
                {column.header}
              </div>
            )}
          </For>
          <Show when={props.expandable}>
            <div class="w-12 px-2"></div>
          </Show>
        </div>
      </div>

      {/* Table Body */}
      <div>
        <For each={props.data}>
          {(item, index) => (
            <div>
              {/* Row */}
              <div
                class={`flex items-center border-b border-gray-200 transition-all duration-200
                        ${props.expandable ? 'cursor-pointer hover:bg-white/15' : ''}
                        ${isRowExpanded(index()) ? 'bg-white/10' : ''}`}
                onClick={() => props.onRowClick?.(item, index())}
                role={props.expandable ? 'button' : undefined}
                tabindex={props.expandable ? 0 : undefined}
                onKeyDown={(e) => {
                  if (props.expandable && (e.key === 'Enter' || e.key === ' ')) {
                    e.preventDefault();
                    props.onRowClick?.(item, index());
                  }
                }}
              >
                <For each={props.columns}>
                  {(column) => (
                    <div class={`px-4 py-3 text-gray-700 text-sm ${column.width || 'flex-1'}`}>
                      <Show
                        when={column.render}
                        fallback={<span>{String(getCellValue(item, column.key as string))}</span>}
                      >
                        {column.render!(item, index())}
                      </Show>
                    </div>
                  )}
                </For>
                <Show when={props.expandable}>
                  <div class="w-12 px-2 flex items-center justify-center">
                    <ChevronDown
                      class={`w-5 h-5 text-gray-600 transition-transform duration-200 rotate-chevron
                              ${isRowExpanded(index()) ? 'expanded' : ''}`}
                    />
                  </div>
                </Show>
              </div>

              {/* Expanded Content */}
              <Show when={props.expandable && isRowExpanded(index()) && props.expandedContent}>
                <div class="bg-white/10 p-6 border-b border-gray-200 animate-fade-in-down">
                  {props.expandedContent!(item, index())}
                </div>
              </Show>
            </div>
          )}
        </For>
      </div>
    </div>
  );
}
