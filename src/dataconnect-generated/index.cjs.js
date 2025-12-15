const { queryRef, executeQuery, mutationRef, executeMutation, validateArgs } = require('firebase/data-connect');

const connectorConfig = {
  connector: 'example',
  service: '7',
  location: 'us-east4'
};
exports.connectorConfig = connectorConfig;

const createPublicListRef = (dcOrVars, vars) => {
  const { dc: dcInstance, vars: inputVars} = validateArgs(connectorConfig, dcOrVars, vars, true);
  dcInstance._useGeneratedSdk();
  return mutationRef(dcInstance, 'CreatePublicList', inputVars);
}
createPublicListRef.operationName = 'CreatePublicList';
exports.createPublicListRef = createPublicListRef;

exports.createPublicList = function createPublicList(dcOrVars, vars) {
  return executeMutation(createPublicListRef(dcOrVars, vars));
};

const getPublicListsRef = (dc) => {
  const { dc: dcInstance} = validateArgs(connectorConfig, dc, undefined);
  dcInstance._useGeneratedSdk();
  return queryRef(dcInstance, 'GetPublicLists');
}
getPublicListsRef.operationName = 'GetPublicLists';
exports.getPublicListsRef = getPublicListsRef;

exports.getPublicLists = function getPublicLists(dc) {
  return executeQuery(getPublicListsRef(dc));
};

const createUserListRef = (dcOrVars, vars) => {
  const { dc: dcInstance, vars: inputVars} = validateArgs(connectorConfig, dcOrVars, vars, true);
  dcInstance._useGeneratedSdk();
  return mutationRef(dcInstance, 'CreateUserList', inputVars);
}
createUserListRef.operationName = 'CreateUserList';
exports.createUserListRef = createUserListRef;

exports.createUserList = function createUserList(dcOrVars, vars) {
  return executeMutation(createUserListRef(dcOrVars, vars));
};

const getUserListsRef = (dc) => {
  const { dc: dcInstance} = validateArgs(connectorConfig, dc, undefined);
  dcInstance._useGeneratedSdk();
  return queryRef(dcInstance, 'GetUserLists');
}
getUserListsRef.operationName = 'GetUserLists';
exports.getUserListsRef = getUserListsRef;

exports.getUserLists = function getUserLists(dc) {
  return executeQuery(getUserListsRef(dc));
};
