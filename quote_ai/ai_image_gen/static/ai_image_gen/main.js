
const app = Vue.createApp({
    data() {
      return {
        includes: false,
        search_list : null,
        search_list_str: null,
        search : '',
        img_tags: null,
        filtered_lists : '',

      }
    },

    // computed:{
      // filtered_lists(){
      //   const searchTerm = this.search.trim().toLowerCase();
      //   return this.search_list.filter((tag) =>
      //   tag.toLowerCase().includes(searchTerm))
      // }
      
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
        created() {
          
          
          
        },

        // when vue is mounted
        mounted(){
          // collected all theme tags to be referenced in the search bar -- unnessary now that I get it from the initial websocket request, but its easier this way. 
          // this.search_list_str = document.getElementById('theme_tag_results_raw').textContent
          // this.search_list = this.search_list_str.split(', ')
          // this.filtered_lists = this.search_list
          // console.log(this.filtered_lists)


          let url = `ws://${window.location.host}/ws/socket-server/`
          const feedSocket = new WebSocket(url)     

          let form = document.getElementById('form')
          form.addEventListener('submit', (e)=>{
            e.preventDefault()
            let message = e.target.elements['search_bar'].value
            console.log(message)
              // validate that the imput is right
              feedSocket.send(JSON.stringify({
                'message':message
              }))
            form.reset()
          })
          
          
          // must be arrow function to get access to the vue object (this.)
          feedSocket.onmessage = (e)=> {
            data = JSON.parse(e.data)
            console.log('websocket message',data)

            // initial connection:
            if (data.type){
              if (data.type == 'DB_Success'){
                console.log('db_connection successful')

                // populating the fields
                this.filtered_lists = data.message
                this.search_list = data.message
                this.search_list_str = ' '+data.message.join(' ')

                // console.log(this.filtered_lists)
              }
              else if (data.type == 'DB_fail'){
                console.log('db_connection failed')
              }
            }

            // on return:
            if (data.source){
                if (data.source == 'fail'){
                  this.img_tags = 'search query failed'
                }
                else if (data.source == 'search'){
                  this.img_tags= data.message.join(', ')
                }
            }
          }
        },
})





app.config.compilerOptions.delimiters = ['$[', ']'];
app.mount('#app')







// To do:
// Get the filtered tag feed to work
// add nore records, 
// on consumers, try for the db querie otherwise return a failed attempt json (otherwise websocket crashes)
// add post mthod with validation, CSRF validation through websocket 
// loading screen, 
// showing the available themes as you type 