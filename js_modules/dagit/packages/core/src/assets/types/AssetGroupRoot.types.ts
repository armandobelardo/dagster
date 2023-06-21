// Generated GraphQL types, do not edit manually.

import * as Types from '../../graphql/types';

export type AssetGroupMetadataQueryVariables = Types.Exact<{
  selector: Types.AssetGroupSelector;
}>;

export type AssetGroupMetadataQuery = {
  __typename: 'WebserverQuery';
  assetNodes: Array<{
    __typename: 'AssetNode';
    id: string;
    autoMaterializePolicy: {
      __typename: 'AutoMaterializePolicy';
      policyType: Types.AutoMaterializePolicyType;
    } | null;
  }>;
};
