// Generated GraphQL types, do not edit manually.

import * as Types from '../../graphql/types';

export type RunTagKeysQueryVariables = Types.Exact<{[key: string]: never}>;

export type RunTagKeysQuery = {
  __typename: 'WebserverQuery';
  runTagKeysOrError:
    | {__typename: 'PythonError'}
    | {__typename: 'RunTagKeys'; keys: Array<string>}
    | null;
};

export type RunTagValuesQueryVariables = Types.Exact<{
  tagKeys: Array<Types.Scalars['String']> | Types.Scalars['String'];
}>;

export type RunTagValuesQuery = {
  __typename: 'WebserverQuery';
  runTagsOrError:
    | {__typename: 'PythonError'}
    | {
        __typename: 'RunTags';
        tags: Array<{__typename: 'PipelineTagAndValues'; key: string; values: Array<string>}>;
      }
    | null;
};
