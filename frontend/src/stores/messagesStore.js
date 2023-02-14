import { defineStore } from "pinia";

export const useMessagesStore = defineStore("messages", {
  state: () => {
    return {
      messages: [],
    };
  },
  getters: {
    messageList() {
      return this.messages;
    },
  },
  actions: {
    /**
     * Display a new message for the user or replace an existing one
     *
     * @param message {Object} Message to display for the user
     * @param message.id {any} Unique id that determines whether this message
     *  will replace an old one.
     * @param message.type {string} Message type: info, success, warning, error
     * @param message.title {string} Message title
     * @param message.description {string} Message body
     */
    addMessage(message) {
      if (message.id) {
        for (let i = 0; i < this.messages.length; i++) {
          if (this.messages[i].id === message.id) {
            this.messages.splice(i, 1, message);
            return;
          }
        }
      }

      this.messages.push(message);
    },
    /**
     * Remove message at the specified index
     * @param index {Number}
     */
    removeMessage(index) {
      this.messages.splice(index, 1);
    },
  },
});
