/**
 * Import function triggers from their respective submodules:
 *
 * import {onCall} from "firebase-functions/v2/https";
 * import {onDocumentWritten} from "firebase-functions/v2/firestore";
 *
 * See a full list of supported triggers at https://firebase.google.com/docs/functions
 */

const functions = require("firebase-functions");
const logger = require("firebase-functions/logger");
const Busboy = require('busboy');
const Readable = require('stream')
const mammoth = require("mammoth");

// Start writing functions
// https://firebase.google.com/docs/functions/typescript

// export const helloWorld = onRequest((request, response) => {
//   logger.info("Hello logs!", {structuredData: true});
//   response.send("Hello from Firebase!");
// });

exports.extractDocument = functions.onRequest(async (request: Request, response: Response) => {
    const fileHandler =  Busboy({ headers: request.headers })
    // Handle fileread
    fileHandler.on('file', (fieldname : string, file : typeof Readable, filename : string, encoding : string, mimetype : string) => {
        if(mimetype === "application/pdf") {
            file.on('data', (data : Buffer) => {
                
            })
        }
        else if(mimetype === "application/msword" || mimetype === "application/vnd.openxmlformats-officedocument.wordprocessingml.document") {
            file.on('data', (data : Buffer) => {
                mammoth.extractRawText({buffer: data}).then((function(result : { value: string}) {
                    const text : string = result.value
                    console.log(text)
                    return {text: text}
                })).catch((err: Error) => {
                    console.log(err)
                    throw new Error('Failed to extract text from Word document');
                })
            })
        }
    })
})