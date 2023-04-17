const app = Vue.createApp({
    data() {
      return {
        includes: false,
        // add all the tag keys here:ß
        search_list : 'nothing so far',

      }
    },
    watch: {
        search(newVal, oldVal) {
        //   console.log(`New message: ${newVal}. Old message: ${oldVal}.`)
          if (this.search_list.includes(' '+newVal)){
            this.includes = true
            console.log(` included `, this.includes)

          }
          else{
            this.includes = false
            console.log(` not included `, this.includes)

          }
        }},
    mounted(){
      console.log('got this far')
      this.search_list = document.getElementById('theme_tag_results_raw').textContent
    }
  })




  
  app.config.compilerOptions.delimiters = ['$[', ']'];
  app.mount('#app')