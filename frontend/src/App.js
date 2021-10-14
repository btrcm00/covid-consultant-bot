import './App.css';
import React, { Component } from 'react';
import ChatBot from './components';
import { ThemeProvider } from 'styled-components';

class App extends Component {
  constructor(props){
    super(props);
    this.state ={
      response: 'Hệ thống đang gặp sự cố, bạn vui lòng chờ vài phút nhe',
    }
    this.theme = {
      background: 'rgba(255, 255, 255, 1)',
      fontFamily: 'Helvetica Neue',
      'border-radius': '10px',
      headerBgColor: 'rgb(70, 138, 150, 1)',
      headerFontColor: '#fff',
      headerFontSize: '25px',
      botBubbleColor: '#fff',
      botFontColor: '#4a4a4a',
      userBubbleColor: 'rgb(70, 138, 150, 0.85)',
      userFontColor: '#fff',
    };
  };

  async predict(text){
    const url = "http://localhost:8000/response";
    const bodyData = JSON.stringify({
      "text" : text
    });
    const reqOpt = {method: "POST", headers: {"Content-type": "application/json"}, body: bodyData};
    await fetch(url, reqOpt)
    .then((resp)=>resp.json())
    .then((respJ)=> {
      this.setState({
        response:respJ.label,
      }, ()=>{
        console.log(respJ.label)
      })
    })
    .catch(()=>{
      this.setState({
        response: 'Hệ thống đang gặp sự cố, bạn vui lòng chờ vài phút nhe',
      })
    })
  };

  async conversationUpdate(conv){
    var conver = "";
    for (let i = 0; i < conv.length; i++) {
      conver += conv[i] + "\n";
    }
    const url = "http://localhost:8000/conversation";
    const bodyData = JSON.stringify({
      "conversation" : conver
    });
    const reqOpt = {method: "POST", headers: {"Content-type": "application/json"}, body: bodyData};
    await fetch(url, reqOpt)
    .then((resp) => resp.json())
    .then((respJ) => {
      console.log('Conversation updated!')
    });
  };

  render(){
    return (
      <div className = "App">
        <header className = "App-header">
        <ThemeProvider theme = {this.theme}>
          <ChatBot
            headerTitle = 'Covid19 chatbot'
            botDelay = {2000}
            userDelay = {1500}
            width = {'500px'}
            height = {'650px'}
            floating = {true}
            hideUserAvatar = {true}
            steps = {[
              {
                id: 'start',
                message: () => {
                  return 'Chào bạn, mình là chatbot hỗ trợ giải đáp thắc mắc cho người dân thành phố Hồ Chí Minh đang phải cách ly tại nhà vì Covid-19. Bạn cần tư vấn về vấn đề gì vậy?'
                },
                trigger: 'user',
              },
              {
                id: 'user',
                user: true,
                trigger: (value)=>{
                  if(!value.value){
                    return 'user'
                  }
                  this.predict(value.value)
                  return 'bot'
                }
              },
              {
                // this step to wait to states updated
                id: 'bot',
                message: 'gypERR!sackError:Col o id nyVisualStuio nstallationtouse',
                trigger: 'bot1'
              },
              {
                // this step to wait to states updated
                id: 'bot1',
                message: 'gypERR!sackError:Col o id nyVisualStuio nstallationtouse',
                trigger: 'reply'
              },
              {
                id: 'reply',
                message: (value)=>{
                  console.log(value.steps);
                  console.log(this.state.response)
                  if (Array.isArray(this.state.response)){
                    console.log(this.state.response[0])
                      return this.state.response[0]
                  }
                  console.log(this.state.response[0])
                  return this.state.response;
                },
                trigger: ()=>{
                  if (Array.isArray(this.state.response) && (this.state.response).length >=2){
                      return 'reply1'
                  }
                  return 'user'
                }
              },
              {
                id: 'reply1',
                message: (value)=>{
                  console.log(this.state.response[1])
                  return this.state.response[1];
                },
                trigger: ()=>{
                  if (Array.isArray(this.state.response) && (this.state.response).length >=3){
                    return 'reply2'
                  }
                  return 'user'
                }
              },
              {
                id: 'reply2',
                message: (value)=>{
                  return this.state.response[2];
                },
                trigger: ()=>{
                  return 'user'
                }
              }
            ]}
          />
          </ThemeProvider>
        </header>
      </div>
    );
  }
}
export default App;
