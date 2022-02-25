const { Botkit } = require('botkit');
const { BotkitCMSHelper } = require('botkit-plugin-cms');

// Import a platform-specific adapter for web.

const { WebAdapter } = require('botbuilder-adapter-web');

const { MongoDbStorage } = require('botbuilder-storage-mongodb');

// Load process.env values from .env file
require('dotenv').config();
    console.log('okoko')
let storage = null;
if (process.env.MONGO_URI) {
    storage = mongoStorage = new MongoDbStorage({
        url : process.env.MONGO_URI,
    });
}
document.write("welcome to Javatpoint");  

const adapter = new WebAdapter({});


const controller = new Botkit({
    webhook_uri: '/api/messages',

    adapter: adapter,

    storage
});

if (process.env.CMS_URI) {
    controller.usePlugin(new BotkitCMSHelper({
        uri: process.env.CMS_URI,
        token: process.env.CMS_TOKEN,
    }));
}
    controller.ready(() => {

        // load traditional developer-created local custom feature modules
        controller.loadModules(__dirname + '/features');

        /* catch-all that uses the CMS to trigger dialogs */
        if (controller.plugins.cms) {
            controller.on('message,direct_message', async (bot, message) => {
                let results = false;
                results = await controller.plugins.cms.testTrigger(bot, message);

                if (results !== false) {
                    // do not continue middleware!
                    return false;
                }
            });
        }
    });