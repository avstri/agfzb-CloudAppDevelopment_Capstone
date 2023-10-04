/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
      const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl(params.COUCH_URL);
      
      try {
        let selector = { state: { $exists: true} };
        if (params.state){
            selector = { state: params.state };
        }
            
        let docs = await getMatchingRecords(cloudant,'dealerships', selector);
        if (docs.result.length<=0){
            if (params.state)
                return {statusCode:404, body:"The state does not exist"};
            else
                return {statusCode:404, body:"The database is empty"};
        }
        
        let lst = docs.result.map(o=>{ return {
          address: o["address"],
          id: o["_id"],
          city: o["city"],
          state: o["state"],
          st: o["st"],
          zip: o["zip"],
          lat: o["lat"],
          long: o["long"],
        }});
        return {dealerships: lst};
      } catch (error) {
          return { statusCode:500, body: error.description };
      }
}

 /*
 Sample implementation to get the records in a db based on a selector. If selector is empty, it returns all records. 
 eg: selector = {state:"Texas"} - Will return all records which has value 'Texas' in the column 'State'
 */
 function getMatchingRecords(cloudant,dbname, selector) {
     return new Promise((resolve, reject) => {
         cloudant.postFind({db:dbname,selector:selector})
                 .then((result)=>{
                   resolve({result:result.result.docs});
                 })
                 .catch(err => {
                    console.log(err);
                     reject({ err: err });
                 });
          })
 }
 
                        
 /*
 Sample implementation to get all the records in a db.
 */
 function getAllRecords(cloudant,dbname) {
     return new Promise((resolve, reject) => {
         cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })            
             .then((result)=>{
               resolve({result:result.result.rows});
             })
             .catch(err => {
                console.log(err);
                reject({ err: err });
             });
         })
 }
