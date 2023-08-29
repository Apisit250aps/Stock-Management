const { createApp, ref } = Vue;

const host = `http://127.0.0.1:8000/`;
const token = '';
const check_user_api = '';



const App = createApp({
  delimiters: ["[{", "}]"],
  data() {
    return {
      fname: "",
      lname: "",
      username: "",
      email: "",
      password: "",
      confirm: "",

      shop_name: "",
      shop_product_type: "",
      shop_address: "",
      shop_sub_district: "",
      shop_district: "",
      shop_province: "",
      shop_post_id: "",
      shop_remark: "",

      shop_tel:"",
      shop_fax:"",

      user_isValid: true,

      user_data: true,

      password_err_msg: "",

      username_isValid: true,
      email_isValid: true,
      fname_isValid: true,
      lname_isValid: true,
      password_isValid: true,


      province_list:null,
      district_list:null,
      sub_district_list:null,

    };
  },
  computed: {},
  mounted() {
    try {
      axios
        .get(get_province_api)
        .then((res)=>{
          this.province_list = res.data['data']
        })
    }
    catch(err){
      console.error(err)
    }


    console.log("loaded!");
  },
  methods: {
    onProvinceChange(){
      const form_data = new FormData;
      form_data.append("csrfmiddlewaretoken", csrf_token);
      form_data.append("province", this.shop_province);
      axios
        .post(get_district_api, form_data)
        .then((res)=>{
          this.district_list = res.data['data']
        })

    },

    showUserData(e) {
      e.preventDefault();

      if (this.user_data) {
        this.user_data = false;
      } else {
        this.user_data = true;
      }
    },
    userCheck(e) {
      e.preventDefault();

      var isValid = true;

      this.fname_isValid = true;
      if (this.fname == "") {
        this.fname_isValid = false;
        isValid = false;
      }

      this.lname_isValid = true;
      if (this.lname == "") {
        this.lname_isValid = false;
        isValid = false;
      }

      this.username_isValid = true;
      if (this.username == "") {
        isValid = false;
        this.username_isValid = false;
      }

      this.email_isValid = true;
      if (this.email == "") {
        isValid = false;
        this.email_isValid = false;
      }

      this.password_isValid = true;
      if (this.password.length < 8) {
        this.password_err_msg = "รหัสสั้นเกินไป";
        this.password_isValid = false;
        isValid = false;
      }
      else {
        if (this.password !== this.confirm) {
          this.password_err_msg = "รหัสผ่านไม่ตรงกัน";
          this.password_isValid = false;
          isValid = false;
        }
      }

      if (isValid) {
        const form_data = new FormData;
        form_data.append("fname", this.fname);
        form_data.append("lname", this.lname);
        form_data.append("username", this.username);
        form_data.append("email", this.email);

        axios
          .post(user_check_api, form_data)
          .then((response) => {
            const data = response.data;
            if (data['status']) {
              this.user_isValid = true;

            }
            else {
              this.user_isValid = false;
              switch (data['message']) {
                case "email":
                  this.email_isValid = false;
                  break;
                case "username":
                  this.username_isValid = false;
                  break;
              }
            }
          })
          
      }
    }
  },
});

App.mount("#app");
