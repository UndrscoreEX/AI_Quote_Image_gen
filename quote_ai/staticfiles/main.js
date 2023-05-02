
const app = Vue.createApp({
    data() {
      return {
        includes: false,
        search_list : null,
        search_list_str: null,
        search : '',
        img_tags: null,
        filtered_lists : '',
        loading: null,
        some_response: null,
        error_message : null,
        result : null,
        img_path : null,
        submissions_remaining : null,

      }
    },

    // computed:{
    // },

    watch: {
        search(newVal) {
          if (this.search_list_str.includes(' '+newVal)){
            this.includes = true
          }

          else{
            this.includes = false
            console.log(` not included `, this.includes)
          }

          // updates of the filtered_lists field. Probably could be added to the computed field but this had a few problems. 
          const searchTerm = this.search.trim().toLowerCase();
          this.filtered_lists = this.search_list.filter((tag) =>
          tag.toLowerCase().includes(searchTerm))
          console.log(this.filtered_lists)
        },
        
      
      },
        
        // when vue is launched
        // created() {
        // },

        // when vue is mounted
        mounted(){
          let url = `ws://${window.location.host}/ws/socket-server/`
          const feedSocket = new WebSocket(url)     

          let form = document.getElementById('form')
          form.addEventListener('submit', (e)=>{
            e.preventDefault()
            this.some_response = false
            let message = e.target.elements['search_bar'].value
            console.log(message)
              // validate that the imput is right
              feedSocket.send(JSON.stringify({
                'message':message
              }))
            form.reset()
            this.loading = true
          })
          
          
          // must be arrow function to get access to the vue object (this.)
          feedSocket.onmessage = (e)=> {
            data = JSON.parse(e.data)
            console.log('websocket message',data)

            // initial connection:
            // type field is only used for DB success/fail control
            if (data.type){
              if (data.type == 'DB_Success'){

                this.submissions_remaining = data.submissions_left
                console.log('db_connection successful')

                // populating the fields at the start
                this.filtered_lists = data.message
                this.search_list = data.message
                this.search_list_str = ' '+data.message.join(' ')

              }
              else if (data.type == 'DB_fail'){
                // *****************
                // maybe add a message for the render to report this
                console.log('db_connection failed')
              }
            }

            // on response from form request:
            if (data.source){
              if (data.source == 'search'){
                this.img_tags= data.message.join(', ')

                // if we got a result from the api
                if (data.result){
                  this.some_response = true

                  // if the DB query worked but the api response was bad
                  if (data.result == 'db_fail'){
                    this.error_message = 'request failed'
                  }
                  // if the DB query worked but there are no tokens left
                  else if (data.result == 'insf_tokens'){
                    this.error_message = 'no tokens left'

                  }

                  // if it worked as expected
                  else{
                    this.img_path = data.result
                    this.submissions_remaining = data.submissions_left
                  }

                  this.loading = false
                  console.log('received')

                }
              }

              // if internal DB search failed
              else if (data.source == 'fail'){
                this.loading = false
                this.img_tags = 'search query failed'
              }
            }


          }
        },
})





app.config.compilerOptions.delimiters = ['$[', ']'];
app.mount('#app')







// To do:
// add more records, 
// add options for Japanese language ones. 
// give 3-5 suggestions of kw that can be clicked. Give option for a random search
// validate the input to avoid XSS
// add post mthod with validation, CSRF validation through websocket 
// figure out the dall e api
// add the 'salt' . i.e 'A dramatic picture that includes the themes of:', 'A pixel art scene of' , 'a scene from a 
// Find how to limit the cookies to 2 picture and count how many have been made
