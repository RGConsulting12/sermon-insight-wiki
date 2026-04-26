/**
 * Map API DTOs → view models. Expand in Phase 2 when wiring screens.
 */

import type { RepositoryInsightFile } from './types';

/** Placeholder: normalize a repository row for table components. */
export function mapRepositoryRow(row: RepositoryInsightFile): RepositoryInsightFile {
  return { ...row };
}
