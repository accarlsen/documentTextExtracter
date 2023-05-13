/**
 * Import function triggers from their respective submodules:
 *
 * import {onCall} from "firebase-functions/v2/https";
 * import {onDocumentWritten} from "firebase-functions/v2/firestore";
 *
 * See a full list of supported triggers at https://firebase.google.com/docs/functions
 */

const logger = require("firebase-functions/logger");
const Busboy = require('busboy');
const Readable = require('stream')
const mammoth = require("mammoth");

// The Cloud Functions for Firebase SDK to create Cloud Functions and triggers.
const { onRequest } = require("firebase-functions/v2/https");
const { onDocumentCreated } = require("firebase-functions/v2/firestore");

// The Firebase Admin SDK to access Firestore.
const { initializeApp } = require("firebase-admin/app");
const { getFirestore } = require("firebase-admin/firestore");

initializeApp();

// Start writing functions
// https://firebase.google.com/docs/functions/typescript

// export const helloWorld = onRequest((request, response) => {
//   logger.info("Hello logs!", {structuredData: true});
//   response.send("Hello from Firebase!");
// });

exports.extractDocument = onRequest(async (request: Request, response: Response) => {
    const fileHandler = Busboy({ headers: request.headers })
    console.log("started")
    // Handle fileread
    fileHandler.on('file', (fieldname: string, file: typeof Readable, filename: string, encoding: string, mimetype: string) => {
        console.log(`File: ${fieldname}`)

        if (mimetype === "application/pdf") {
            file.on('data', (data: Buffer) => {
                console.log("pdf detected")

            }).on('close', () => {
                console.log(`closedqe`);
            });
        }
        else if (mimetype === "application/msword" || mimetype === "application/vnd.openxmlformats-officedocument.wordprocessingml.document") {
            file.on('data', (data: Buffer) => {
                mammoth.extractRawText({ buffer: data }).then((function (result: { value: string }) {
                    const text: string = result.value
                    console.log(text)
                    return { text: text }
                })).catch((err: Error) => {
                    console.log(err)
                    throw new Error('Failed to extract text from Word document');
                })
            }).on('close', () => {
                console.log(`closedqe`);
            });
        }
    })
})