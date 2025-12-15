import { ConnectorConfig, DataConnect, QueryRef, QueryPromise, MutationRef, MutationPromise } from 'firebase/data-connect';

export const connectorConfig: ConnectorConfig;

export type TimestampString = string;
export type UUIDString = string;
export type Int64String = string;
export type DateString = string;




export interface CreatePublicListData {
  list_insert: List_Key;
}

export interface CreatePublicListVariables {
  name: string;
  description?: string | null;
}

export interface CreateUserListData {
  list_insert: List_Key;
}

export interface CreateUserListVariables {
  name: string;
  description?: string | null;
}

export interface GetPublicListsData {
  lists: ({
    id: UUIDString;
    name: string;
    description?: string | null;
    createdAt: TimestampString;
    updatedAt: TimestampString;
  } & List_Key)[];
}

export interface GetUserListsData {
  lists: ({
    id: UUIDString;
    name: string;
    description?: string | null;
    createdAt: TimestampString;
    updatedAt: TimestampString;
  } & List_Key)[];
}

export interface ListMovie_Key {
  listId: UUIDString;
  movieId: UUIDString;
  __typename?: 'ListMovie_Key';
}

export interface List_Key {
  id: UUIDString;
  __typename?: 'List_Key';
}

export interface Movie_Key {
  id: UUIDString;
  __typename?: 'Movie_Key';
}

export interface Review_Key {
  id: UUIDString;
  __typename?: 'Review_Key';
}

export interface User_Key {
  id: UUIDString;
  __typename?: 'User_Key';
}

export interface Watch_Key {
  id: UUIDString;
  __typename?: 'Watch_Key';
}

interface CreatePublicListRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreatePublicListVariables): MutationRef<CreatePublicListData, CreatePublicListVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: CreatePublicListVariables): MutationRef<CreatePublicListData, CreatePublicListVariables>;
  operationName: string;
}
export const createPublicListRef: CreatePublicListRef;

export function createPublicList(vars: CreatePublicListVariables): MutationPromise<CreatePublicListData, CreatePublicListVariables>;
export function createPublicList(dc: DataConnect, vars: CreatePublicListVariables): MutationPromise<CreatePublicListData, CreatePublicListVariables>;

interface GetPublicListsRef {
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<GetPublicListsData, undefined>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect): QueryRef<GetPublicListsData, undefined>;
  operationName: string;
}
export const getPublicListsRef: GetPublicListsRef;

export function getPublicLists(): QueryPromise<GetPublicListsData, undefined>;
export function getPublicLists(dc: DataConnect): QueryPromise<GetPublicListsData, undefined>;

interface CreateUserListRef {
  /* Allow users to create refs without passing in DataConnect */
  (vars: CreateUserListVariables): MutationRef<CreateUserListData, CreateUserListVariables>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect, vars: CreateUserListVariables): MutationRef<CreateUserListData, CreateUserListVariables>;
  operationName: string;
}
export const createUserListRef: CreateUserListRef;

export function createUserList(vars: CreateUserListVariables): MutationPromise<CreateUserListData, CreateUserListVariables>;
export function createUserList(dc: DataConnect, vars: CreateUserListVariables): MutationPromise<CreateUserListData, CreateUserListVariables>;

interface GetUserListsRef {
  /* Allow users to create refs without passing in DataConnect */
  (): QueryRef<GetUserListsData, undefined>;
  /* Allow users to pass in custom DataConnect instances */
  (dc: DataConnect): QueryRef<GetUserListsData, undefined>;
  operationName: string;
}
export const getUserListsRef: GetUserListsRef;

export function getUserLists(): QueryPromise<GetUserListsData, undefined>;
export function getUserLists(dc: DataConnect): QueryPromise<GetUserListsData, undefined>;

