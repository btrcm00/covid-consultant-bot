import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Bubble from './Bubble';
import Image from './Image';
import ImageContainer from './ImageContainer';
import Loading from '../common/Loading';
import TextStepContainer from './TextStepContainer';

class TextStep extends Component {
  /* istanbul ignore next */
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
    };
  }

  componentDidMount() {
    const { step, triggerNextStep } = this.props;
    const { component, delay, waitAction } = step;
    const isComponentWatingUser = component && waitAction;
    let a = step.id === 'start' ? 0 : delay;
    if(step.id === 'bot'){
      a = 1000;
    }
    else if(step.id === 'bot1'){
      a = 2000
    }

    setTimeout(() => {
      this.setState({ loading: false }, () => {
        if (!isComponentWatingUser && !step.rendered) {
          triggerNextStep();
        }
      });
    }, a);
  }
  capitalizeFirstLetter = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }
  getMessage = () => {
    const { previousValue, step } = this.props;
    var { message, uploading } = step;
    if(uploading){
      message = message[0]
      return message ? message.replace(/{previousValue}/g, previousValue) : '';
    }
    if(message.split("/").length>2){
      return message;
    }
    
    return message ? this.capitalizeFirstLetter(message.replace(/{previousValue}/g, previousValue)) : '';
  };

  renderMessage = () => {
    const { step, steps, previousStep, triggerNextStep } = this.props;
    const { component } = step;
    if (component) {
      return React.cloneElement(component, {
        step,
        steps,
        previousStep,
        triggerNextStep
      });
    }
    return this.getMessage();
  };

  render() {
    const {
      step,
      isFirst,
      isLast,
      avatarStyle,
      bubbleStyle,
    } = this.props;
    const { loading } = this.state;
    const { avatar, user, botName } = step;

    const imageAltText = user ? "Your avatar" : `${botName}'s avatar`;

    return (
      <TextStepContainer className={`rsc-ts ${user ? 'rsc-ts-user' : 'rsc-ts-bot'}`} user={user}>
        <ImageContainer className="rsc-ts-image-container" user={user}>
          {this.renderMessage()!=='GypERR!sackError:Col o id nyVisualStuio nstallationtouse' && !user&&(
            <Image
              className="rsc-ts-image"
              style={avatarStyle}
              user={user}
              src={avatar}
              alt={imageAltText}
            />
          )
          }
        </ImageContainer>
        {this.renderMessage()!=='GypERR!sackError:Col o id nyVisualStuio nstallationtouse'&&
        <Bubble
          className="rsc-ts-bubble"
          style={bubbleStyle}
          user={user}
          isFirst={isFirst}
          isLast={isLast}
        >
          {loading ? <Loading /> : this.renderMessage()}
        </Bubble>}
      </TextStepContainer>
    );
  }
}

TextStep.propTypes = {
  avatarStyle: PropTypes.objectOf(PropTypes.any).isRequired,
  isFirst: PropTypes.bool.isRequired,
  isLast: PropTypes.bool.isRequired,
  bubbleStyle: PropTypes.objectOf(PropTypes.any).isRequired,
  previousStep: PropTypes.objectOf(PropTypes.any),
  previousValue: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.bool,
    PropTypes.number,
    PropTypes.object,
    PropTypes.array
  ]),
  step: PropTypes.objectOf(PropTypes.any).isRequired,
  steps: PropTypes.objectOf(PropTypes.any),
  triggerNextStep: PropTypes.func.isRequired
};

TextStep.defaultProps = {
  previousStep: {},
  previousValue: '',
  steps: {}
};

export default TextStep;
