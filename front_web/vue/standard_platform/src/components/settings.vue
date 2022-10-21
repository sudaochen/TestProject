<template>
  <div id="app">
    <button @click="connect">Connect</button><br><br><br>
    <button @click="send">Send</button><br><br><br>
    <button @click="emit">Emit</button><br><br><br>


  </div>
</template>

<script>
import { io } from "socket.io-client";

export default {
  name: 'App',
  data() {
    return {
      socket: io('http://localhost:5000/')
    }
  },
  methods: {
    connect() { 
     this.socket.emit('ensureconnect','ensure connect')
     },

    send() {
      this.socket.send('send')
    },

    emit(){
      this.socket.emit('emit', 'popen_test')
      
    },

    
  },
  mounted(){
    this.socket.on("emit",async function(data){
      console.log(data)
    })
  }
}
</script>











