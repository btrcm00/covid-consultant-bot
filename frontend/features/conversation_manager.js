const debug = require("debug")("botkit:domains");
const request = require("request-promise");
const schedule = require('node-schedule');

const limits = new Map();

var UserState = {};
var AdminState = {};
const pLimit = require('p-limit');

var url ='http://0.0.0.0:8000/api/send-message'
var image_url = 'http://0.0.0.0:8000/api/send-image' ;
var message_queue = {};
var id_job_js = {};
var image_queue = {};
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
async function callMessageAPI(options,message,bot){
    const ref = message.reference;
    await bot.changeContext(ref);
    if ((message.user) in message_queue && message.text ){
      message_queue[message.user].push(message.text);
    }
    else if (message.text){
      message_queue[message.user] = [message.text];
    }
   
    var jobList = schedule.scheduledJobs;
    var send_time = new Date().addSeconds(6);
    console.log("SEND TIME");
    console.log(send_time);
    var job = 'jobList.SendingSpan' + String(id_job_js[message.user]);
    if (eval(job) != undefined){
      eval(job +'.cancel()')};
    const tmp_schedule = schedule.scheduleJob('SendingSpan'+  String(id_job_js[message.user]), send_time, async function (bot,message){
      message_queue[message.user] = [];
      image_queue[message.user] = '';
      async function impl (options,message,bot){
        const ref = message.reference;
        await bot.changeContext(ref);
      await request(options, async function (error, response) {
        if (error) throw new Error(error);
        suggest_reply = JSON.parse(response.body)["suggest_reply"];
        id_job = JSON.parse(response.body)["id_job"];
        check_end  = JSON.parse(response.body)["check_end"];
        rep_intent = JSON.parse(response.body)["rep_intent"];
        if (suggest_reply){
          var job = 'jobList.RemindMess' + (id_job);
          if (eval(job) != undefined){
            eval(job +'.cancel()')
          };
          for (var sentence of suggest_reply.split("*")){
            bot.reply(message, sentence);
            await sleep(1500);
          }
        }
      });
      tmp_schedule.cancel();
    }
      const { id } = message.user // or similar to distinguish them
      if (!limits.has(id)) {
        limits.set(id, pLimit(1)); // only one active request per user
      }
      const limit = limits.get(id);
      return limit(impl, options,message,bot); // schedule impl for execution

  }.bind(null,bot,message));
}

defaultUserState = (ref) => ({
  subscriber: [],
  ref: ref,
});

defaultAdminState = (ref) => ({
  subscriber: [],
  ref: ref,
});

function s4() {
  // GENERATE RANDOM ID
  return Math.floor((1 + Math.random()) * 0x10000)
      .toString(16)
      .substring(1);
}

function createUserState(m) {
  for (let u in UserState) {
    if (m.user === u) {
      return UserState[u];
    }
  }
  return defaultUserState(m.reference);
}

function createAdminState(m) {
  for (let u in AdminState) {
    if (m.user === u) {
      return AdminState[u];
    }
  }
  return defaultAdminState(m.reference);
}

function getUserState(m) {
  for (let u in UserState) {
    if (m === u) {
      return UserState[u];
    }
  }
  return null;
}

function getAdminState(m) {
  for (let u in AdminState) {
    if (m === u) {
      return AdminState[u];
    }
  }
  return null;
}



module.exports = function (controller) {
  // controller.middleware.receive.use(rasa.receive);

  const onMessage = async (bot, message) => {
    //console.log(message);
    var suggest_reply = '';
    var id_job = '';
    if (!(message.user in id_job_js)){
      id_job_js[message.user] = Object.keys(id_job_js).length+1;
    }
    if (message.image || (message.user in image_queue && image_queue[message.user])){
      // console.log(message.image);
      if (message.user in message_queue && message_queue[message.user].length>0){
        var mess_text = message_queue[message.user].join('.') +"." + message.text;
      }
      else if (message.text)
        var mess_text = message.text;
      else
        var mess_text = '';

      if (message.user in image_queue && image_queue[message.user].length > 0 && message.image){
          image_queue[message.user].push(message.image.split(',')[1]);
          var list_image = image_queue[message.user];
      }
      else if(message.image) {
          var list_image = [message.image.split(',')[1]];
          image_queue[message.user] = [message.image.split(',')[1]];
      }
      else 
          var list_image = image_queue[message.user];
      console.log("LENGTH OF IMAGE QUEUE");
      console.log(image_queue[message.user].length);        

      console.log("----------BASE64 của ảnh--------");
      var options = {
        'method': 'POST',
        'url': image_url,
        'headers':{},
        formData: {
          'sender_id': message.user,
          'recipient_id': 'admin',
          'mid': s4() + s4() + "-" + s4() + "-" + s4() + "-" + s4() + "-" + s4() + s4() + s4(),
          'image[]': list_image,
          'text': mess_text
        }
      };

      callMessageAPI(options,message,bot);

    }
    else {
      if (message.user in message_queue && message_queue[message.user].length>0){
        var mess_text = message_queue[message.user].join('.') +"." + message.text;
      }
      else
        var mess_text = message.text;
      
      var options = {
        'method': 'POST',
        'url': url,
        'headers': {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        formData: {
          'sender_id': message.user,
          'recipient_id': 'admin',
          'mid': s4() + s4() + "-" + s4() + "-" + s4() + "-" + s4() + "-" + s4() + s4() + s4(),
          'text': mess_text,
        }
      };
      callMessageAPI(options,message,bot);
    }
    
    
  };

  const onWelcomeBack = async (bot, message) => {
    debug("Welcome back");
    UserState[message.user] = await createUserState(message);
    UserState[message.user+'check_respones'] = true;
    await bot.reply(message, "Xin chào, mình là Covid Chatbot. Bạn cần mình tư vấn gì hong,");
  };

  const onHelloClient = async (bot, message) => {
    debug("Welcome back");
    UserState[message.user] = await createUserState(message);
    UserState[message.user+'check_respones'] = true;

    await bot.reply(message, "Xin chào, mình là Covid Chatbot. Bạn cần mình tư vấn gì hong nè");
  };

  const onHelloAdmin = async (bot, message) => {
    AdminState[message.user] = await createAdminState(message);
    await bot.reply(message, "Xin chào admin");
    let reply = [];
  
    for (let u in UserState) {
        reply.push({
          title: u,
          payload: `subscribe ${u}`,
        });
    }
    await bot.reply(message, {
      text: "Hệ thống hiện có các khách hàng sau",
      quick_replies: reply,
    });
  };

  const onAdminMessage = async (bot, message) => {
    console.log(message.text);
  }

  controller.on("welcome_back", onWelcomeBack);
  controller.on("hello", onWelcomeBack);
  controller.on("client_hello", onHelloClient);
  // controller.on("image", onImage);
  controller.on("message", onMessage);
  controller.on("admin_hello", onHelloAdmin);
  controller.on("admin_message", onAdminMessage);
  // controller.on("image", imageProcess);
};  