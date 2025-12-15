import { CreatePublicListData, CreatePublicListVariables, GetPublicListsData, CreateUserListData, CreateUserListVariables, GetUserListsData } from '../';
import { UseDataConnectQueryResult, useDataConnectQueryOptions, UseDataConnectMutationResult, useDataConnectMutationOptions} from '@tanstack-query-firebase/react/data-connect';
import { UseQueryResult, UseMutationResult} from '@tanstack/react-query';
import { DataConnect } from 'firebase/data-connect';
import { FirebaseError } from 'firebase/app';


export function useCreatePublicList(options?: useDataConnectMutationOptions<CreatePublicListData, FirebaseError, CreatePublicListVariables>): UseDataConnectMutationResult<CreatePublicListData, CreatePublicListVariables>;
export function useCreatePublicList(dc: DataConnect, options?: useDataConnectMutationOptions<CreatePublicListData, FirebaseError, CreatePublicListVariables>): UseDataConnectMutationResult<CreatePublicListData, CreatePublicListVariables>;

export function useGetPublicLists(options?: useDataConnectQueryOptions<GetPublicListsData>): UseDataConnectQueryResult<GetPublicListsData, undefined>;
export function useGetPublicLists(dc: DataConnect, options?: useDataConnectQueryOptions<GetPublicListsData>): UseDataConnectQueryResult<GetPublicListsData, undefined>;

export function useCreateUserList(options?: useDataConnectMutationOptions<CreateUserListData, FirebaseError, CreateUserListVariables>): UseDataConnectMutationResult<CreateUserListData, CreateUserListVariables>;
export function useCreateUserList(dc: DataConnect, options?: useDataConnectMutationOptions<CreateUserListData, FirebaseError, CreateUserListVariables>): UseDataConnectMutationResult<CreateUserListData, CreateUserListVariables>;

export function useGetUserLists(options?: useDataConnectQueryOptions<GetUserListsData>): UseDataConnectQueryResult<GetUserListsData, undefined>;
export function useGetUserLists(dc: DataConnect, options?: useDataConnectQueryOptions<GetUserListsData>): UseDataConnectQueryResult<GetUserListsData, undefined>;
