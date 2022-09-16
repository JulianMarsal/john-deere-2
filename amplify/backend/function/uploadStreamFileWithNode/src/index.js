/* Amplify Params - DO NOT EDIT
    ENV
    REGION
Amplify Params - DO NOT EDIT */
// const { Upload } = require("@aws-sdk/lib-storage");
// const { S3Client, S3 } = require("@aws-sdk/client-s3");
// const axios = require('axios');
// const fs = require('fs')


// const Bucket = 'johndeere-layers152031-staging';
// const header = {
//     'Accept': 'application/vnd.deere.axiom.v3+json',
//     "Authorization": process.env.Authorization
// }
// exports.handler = async function (context, event, callback) {
//     const fileUrl = "https://sandboxapi.deere.com/platform/fieldOps/NTg3NDU2XzYyZjUxMGVmYjEyNWRkOTBkM2ViOGQ4Mw";
//     let stream
//     const response = await axios({
//         url: fileUrl,
//         method: 'GET',
//         responseType: 'stream',
//         headers: header
//     })
//     response.data.pipe(stream);
//     //const response = await axios("https://sandboxapi.deere.com/platform/fieldOps/NTg3NDU2XzYyZjUxMGVmYjEyNWRkOTBkM2ViOGQ4Mw")
//     console.log("response datita : " + response.data)
//     try {
//         // const parallelUploads3 = new Upload({
//         //     client: new S3({
//         //         accessKeyId: process.env.accessKeyId,
//         //         secretAccessKey: process.env.secretAccessKey,
//         //     }) || new S3Client({
//         //         region: "us-east-1", credentials: {
//         //             accessKeyId: 'process.env.accessKeyId',
//         //             secretAccessKey: 'process.env.secretAccessKey'
//         //         }
//         //     }),

//         const parallelUploads3 = new Upload({
//             client: new S3Client({
//                 region: "us-east-1",
//                 credentials: {
//                     accessKeyId: process.env.accessKeyId,
//                     secretAccessKey: process.env.secretAccessKey
//                 }
//             }),
//             params: { Bucket: Bucket, Key: "UploadDePruebaStream2", Body: stream },

//             tags: [
//                 /*...*/
//             ], // optional tags
//             queueSize: 4, // optional concurrency configuration
//             partSize: 1024 * 1024 * 5, // optional size of each part, in bytes, at least 5MB
//             leavePartsOnError: false, // optional manually handle dropped parts
//         });

//         parallelUploads3.on("httpUploadProgress", (progress) => {
//             console.log(progress);
//         });

//         await parallelUploads3.done();
//     } catch (e) {
//         console.log(e);
//     }
//     return "algo"
// }








const axios = require('axios');
let AWS = require('aws-sdk');
const S3UploadStream = require('s3-upload-stream');

//For rirdes add 'Accept': 'application/octet-stream', for files only Authorization
const header = {
    'Accept': 'application/zip',
    "Authorization": process.env.Authorization
}

exports.handler = async function (context, event, callback) {


    // Set the region
    AWS.config.update({ region: 'us-west-2' });
    AWS.config.update({ accessKeyId: context.AWSaccessKeyId, secretAccessKey: context.AWSsecretAccessKey });

    // The name of the bucket that you have created
    const BUCKET_NAME = 'johndeere-layers152031-staging';

    const fileUrl = "https://sandboxapi.deere.com/platform/files/51475183645";
    const fileName = "pruebaFiles2_2.zip";

    const s3Stream = S3UploadStream(new AWS.S3({
        region: "us-east-1",
        credentials: {
            accessKeyId: process.env.accessKeyId,
            secretAccessKey: process.env.secretAccessKey
        }
    }));

    // call S3 to retrieve upload file to specified bucket
    let upload = s3Stream.upload({ Bucket: BUCKET_NAME, Key: fileName, ContentType: 'image/jpeg.zip', ACL: 'public-read' });

    const fileUpload = await uploadFile(fileUrl, upload)
        .then(result => callback(null, `success: ${JSON.stringify(result)}`))
        .catch(err => callback(err.message));

    async function uploadFile(url, upload) {

        const response = await axios({
            url: fileUrl,
            method: 'GET',
            responseType: 'stream',
            headers: header
        })

        response.data.pipe(upload);

        return new Promise((resolve, reject) => {
            upload.on('uploaded', resolve)
            upload.on('error', reject)
        })
    }
    console.log("fileUpload")
    callback(null, fileUpload)
};