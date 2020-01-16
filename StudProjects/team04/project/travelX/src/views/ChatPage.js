import React, { Component } from "react";
import { Button } from 'antd';
import { Input } from 'antd';

import "./ChatPage.scss";
import hotelSearch, { qa } from "../repository/hotelSearchRepo";
const axios = require('axios');

const { TextArea } = Input;

class ChatPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            currentMessage: "",
            messages: [{ text: "Hi! My name is Gelu and I'm a your travel assistant. Please type in your trip details.", from: "ai" }],
            disabled: false,
            document: ""
        }
    }

    componentDidMount() {
    }

    _handleKeyDown = (e) => {
        if (e.key === "Enter") {
            this.setState({})
        }
    };

    _addToChat = () => {
        if (this.state.currentMessage.trim() === "") {
            return;
        }

        let messages = this.state.messages;
        messages.push({ text: this.state.currentMessage, from: "user" });
        messages.push({ text: "", from: "ai", class: "loading" });
        this.setState({ messages: messages, currentMessage: "", disabled: true });

        if (this.state.document === "") {
            this._sendQuestion(this.state.currentMessage)
                .then(({ data }) => {
                    messages.pop();
                    // messages.push({ text: `Hotel: ${data.title} Answer: "${data.answer}" Context: "${data.paragraph}"`, from: "ai" });
                    messages.push({ text: `${data.answer}`, from: "ai" });

                    if (data.doSearch) {
                        hotelSearch(data.searchQuery)
                            .then((resp) => {
                                messages.push({ text: `Check out this hotel: <img width="230px" src="${resp.url}" />${resp.name}`, from: "ai" });
                                this.setState({ messages: messages, disabled: false, document: resp.description || "" });
                            })
                            .catch(() => {
                                this.setState({ messages: messages, disabled: false });
                            });
                    } else {
                        this.setState({ messages: messages, disabled: false });
                    }
                })
                .catch(() => {
                    messages.pop();
                    messages.push({ text: "Sorry, didn't get that.", from: "ai" });
                    this.setState({ messages: messages, disabled: false });
                })
                .finally(() => {
                    let elem = document.getElementById('message-container');
                    let textArea = document.getElementById('textarea');
                    elem.scrollTop = elem.scrollHeight;
                    textArea.focus();
                });
        } else {
            qa(this.state.document, this.state.currentMessage)
                .then((resp) => {
                    messages.pop();
                    messages.push({ text: `${resp}`, from: "ai" });
                    this.setState({ messages: messages, disabled: false });
                })
                .catch(() => {
                    messages.pop();
                    messages.push({ text: "Sorry, I can't find that information :(", from: "ai" });
                    this.setState({ messages: messages, disabled: false });
                })
                .finally(() => {
                    let elem = document.getElementById('message-container');
                    let textArea = document.getElementById('textarea');
                    elem.scrollTop = elem.scrollHeight;
                    textArea.focus();
                });
        }
    };

    _onMessageValueChange = (e) => {
        this.setState({ currentMessage: e.target.value });
    };

    _sendQuestion = (text) => {
        return axios.get(`http://localhost:5000/api`, {
            params: {
                query: text
            }
        });
    };

    render() {
        return (
            <div className="chat-main">
                <div className="message-container" id="message-container">
                    {this.state.messages.map(message =>
                        <div><div className={`speech-bubble ${message.from} ${message.class}`} dangerouslySetInnerHTML={{ __html: message.text }}></div></div>
                    )}
                </div>
                <div className="footer">
                    <TextArea
                        id="textarea"
                        autoFocus
                        placeholder="Type here"
                        value={this.state.currentMessage}
                        autoSize={{ minRows: 1, maxRows: 3 }}
                        onPressEnter={() => this._addToChat()}
                        onChange={(e) => this._onMessageValueChange(e)}
                        disabled={this.state.disabled}
                    />
                    <Button type="primary" shape="circle" icon="arrow-right" size={"large"} onClick={() => this._addToChat()} />
                </div>
            </div>
        );
    }
}

export default ChatPage;
