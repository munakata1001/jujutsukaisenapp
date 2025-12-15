# Basic Usage

Always prioritize using a supported framework over using the generated SDK
directly. Supported frameworks simplify the developer experience and help ensure
best practices are followed.





## Advanced Usage
If a user is not using a supported framework, they can use the generated SDK directly.

Here's an example of how to use it with the first 5 operations:

```js
import { createPublicList, getPublicLists, createUserList, getUserLists } from '@dataconnect/generated';


// Operation CreatePublicList:  For variables, look at type CreatePublicListVars in ../index.d.ts
const { data } = await CreatePublicList(dataConnect, createPublicListVars);

// Operation GetPublicLists: 
const { data } = await GetPublicLists(dataConnect);

// Operation CreateUserList:  For variables, look at type CreateUserListVars in ../index.d.ts
const { data } = await CreateUserList(dataConnect, createUserListVars);

// Operation GetUserLists: 
const { data } = await GetUserLists(dataConnect);


```