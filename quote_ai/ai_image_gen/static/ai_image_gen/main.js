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
        response_content : null,
        feedSocket : null,
        cur_book: null,
        cur_author: null,
        cur_quote : null,
        cur_theme_tag: null,
        cur_chosen_theme_tag : null ,
        cur_image_tag : null,
        dall_e_image : null,
        prompt_used: null,
        toggle : false,
        error_reason : null,
        ready_to_send: false,
        opened_examples : [],


      }
    },

    computed:{
     
    },

    watch: {
        search(newVal) {
          if (newVal){
            let capNewVal = newVal[0].toLowerCase() + newVal.slice(1)
            if (this.search_list_str.includes(' '+capNewVal)){
              this.includes = true
            }
  
            else{
              this.includes = false
              console.log(capNewVal)
              console.log(` not included `, this.includes)
            }

          }

          // :: updates of the filtered_lists field. Probably could be added to the computed field but this had a few problems. 
          let searchTerm = this.search.trim().toLowerCase();
          this.filtered_lists = this.search_list.filter((tag) =>
          tag.toLowerCase().includes(searchTerm))

          // :: randomize the results
          this.filtered_lists = this.filtered_lists.sort(() => .5 - Math.random())
          console.log('key pressed, this is the list associated with the string so far: ',this.filtered_lists)
        },
        
      
      },
        
        // :: when vue is mounted
        mounted(){
          let url = `ws://${window.location.host}/ws/socket-server/`
          this.feedSocket = new WebSocket(url)     

          let form = document.getElementById('form')
          form.addEventListener('submit', (e)=>{
            e.preventDefault()
            let message = e.target.elements['search_bar'].value

            // validating if the message is correct 
            if ((this.search_list_str.includes(' '+message+' '))){
              this.loading = true
              // :: start the loading gif
              console.log('loading is true::::')
              this.some_response = false
              this.error_message = null
              // console.log('message that is sent up to the consumer: ',message)
              this.feedSocket.send(JSON.stringify({
                'message':message
              })) 
            }
            else{
              console.log('not a valied term')
              this.error_message = 'Theme not available. Try another valid option'
              this.some_response = true
            }
            form.reset()

          })
          
          
          // :: must be arrow function to get access to the vue object (this.)
          this.feedSocket.onmessage = (e)=> {
            data = JSON.parse(e.data)
            console.log('websocket message',data)

            // :: initial connection:
            // :: type field is only used/checked for DB success/fail control
              if (data.type && data.type == 'DB_Success'){
                this.submissions_remaining = data.submissions_left
                console.log('db_connection successful')

                // :: populating the fields at the start
                this.search_list = data.message
                this.search_list_str = ' '+data.message.join(' ')
                // :: randomize the results
                this.filtered_lists = data.message.sort(() => .5 - Math.random())

              }
              else if (data.type && data.type == 'DB_fail'){
                this.error_message = 'initial DB_connection failed'
                console.log('db_connection failed')
              }

            // :: on response from form request:
            if (data.source && data.source == 'search'){
                this.img_tags= data.message.join(', ')

                this.cur_book = data.query_content.book

                // :: Sanitizing the quote that I get from the DB to allow the <br> tags to take effect.
                // :: connects with the v-html tag in the render
                this.cur_quote = DOMPurify.sanitize(data.query_content.quote, {
                  ALLOWED_TAGS: ['br'],
                });

                this.cur_theme_tag = data.query_content.all_themes
                this.cur_chosen_theme_tag = data.query_content.chosen_theme
                this.cur_image_tag = data.query_content.img_tags
                this.cur_author = data.query_content.author
                console.log(this.cur_quote)
                
                // :: if we got a result from the api
                if (data.result) {
                  switch (data.result) {
                    case 'db_fail':
                      this.some_response = true
                      this.error_message = 'request failed'
                      break
                    case 'insf_tokens':
                      this.some_response = true
                      this.error_message = 'no tokens left'
                      this.loading = false
                      break
                    default:
                      this.some_response = true
                      this.img_path = data.result
                      this.dall_e_image = data.dall_e_image
                      this.submissions_remaining = data.submissions_left
                      this.loading = false
                      this.prompt_used = data.prompt_used
                      console.log('loading is turned off now :::::')
                      break
                  }

                  // :: end the loading gif because a responsse was obtained 
                  // this.loading = false

                }
                
              }

              // :: if internal DB search failed
              else if (data.source && data.source == 'fail'){
                this.loading = false
                this.some_response = true

                this.error_message = 'search query failed'
                this.error_reason = data.reason
              }
            // }


          }
        },

        methods : {
          search_keyword(kw) {
            console.log('sending', kw)
            console.log(this.submissions_remaining, this.img_tags, this.search_list_str)
            this.feedSocket.send(JSON.stringify({
              'message':kw
            }))
            this.loading = true
            this.some_response = false

            // :: start the loading gif
            console.log('loading is true::::')

  
          },
          start_loading() {
            console.log('loading is set to True')
            this.loading = true
          },
          addToOpenedExamples(index) {
            console.log(index)
            if (!this.opened_examples.includes(index)){
              this.opened_examples.push(index);
            }
            else if (this.opened_examples.includes(index)){
              this.opened_examples.splice(this.opened_examples.indexOf(index), 1);
            }
          },
          clean_quote(quote_text){
            if (quote_text.length > 80 ){
              quote_text = quote_text.slice(0,80)+'...'
              
            }
            this.quote_text = DOMPurify.sanitize(quote_text, {
              ALLOWED_TAGS: ['br'],
            });
            return quote_text
          }
        }
})




app.config.compilerOptions.delimiters = ['$[', ']'];
app.mount('#app')







// To do:
// add wwaaaaaaay more image words
// write tests 
// Decouple and add more functions/ classses for everything
// make it look better
// low priority - add options for Japanese language ones.
// Add dynamic elements the carousel and the card.


