<template>
  <div id="addGoods">
    <div class="h1">{{title}}</div>
    <div class="form_box">
      <i-form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="150">
        <FormItem label="图片选择" prop="image_data">
          <div class="imgSelectBox">
            <div class="index">
              <ul>
                <li
                  v-for="imgNo in formValidate.image_data"
                  :key="imgNo.img_url"
                  v-bind:class="[imgNo.is_min ? 'isActive' : '']"
                >
                  <img :src="imgNo.img_url" alt>
                  <div class="div">
                    <p v-on:click="imgShowFun(imgNo)">
                      <Icon type="ios-eye"/>
                    </p>
                    <p v-on:click="imgDelFun(imgNo)">
                      <Icon type="md-close"/>
                    </p>
                    <p v-on:click="imgOnFun(imgNo)">
                      <Icon type="md-checkmark"/>
                    </p>
                  </div>
                </li>
                <li>
                  <Upload
                    ref="upload"
                    :show-upload-list="false"
                    :format="['jpg','jpeg','png']"
                    :on-success="imgUpData"
                    name="image"
                    :action="path"
                    multiple
                    type="drag"
                    style="display: inline-block;width:83px;"
                  >
                    <div style="width: 83px;height:83px;line-height: 93px;">
                      <Icon type="ios-cloud-upload" size="30"></Icon>
                    </div>
                  </Upload>
                </li>
              </ul>
            </div>
          </div>
        </FormItem>
        <FormItem label="商品标题" prop="name">
          <i-input v-model="formValidate.name" style="width:650px;" placeholder="请输入商品标题"></i-input>
        </FormItem>
        <!-- <FormItem label="分类" prop="tag_id">
          <Select v-model="formValidate.tag_id" style="width:650px;" placeholder="请选择分类">
            <Option
              v-for="item in formClassList"
              v-if="item.is_show==='1'"
              :key="item.id"
              :value="item.id"
            >{{item.name}}</Option>
          </Select>
        </FormItem>-->
        <FormItem label="钢镚价" prop="price">
          <Poptip trigger="focus">
            <div slot="content">{{ formValidate_price }}</div>
            <i-input v-model="formValidate.price" style="width:650px;" placeholder="请输入价格"></i-input>
          </Poptip>
        </FormItem>
        <FormItem label="邮费" prop="postage">
          <Poptip trigger="focus">
            <div slot="content">{{ formValidate_postage }}</div>
            <i-input v-model="formValidate.postage" style="width:650px;" placeholder="请输入运费"></i-input>
          </Poptip>
        </FormItem>
        <FormItem label="库存" prop="ku_num">
          <i-input v-model="formValidate.ku_num" style="width:650px;" placeholder="请输入库存"></i-input>
        </FormItem>
        <FormItem label="商品详情" prop="detail">
          <div ref="editor" class="detail">
            <quill-editor v-model="formValidate.detail" ref="myQuillEditor" :options="editorOption">
              <div id="toolbar" slot="toolbar">
                <!--图片按钮点击事件-->
                <span class="ql-formats">
                  <button type="button" @click="clickupdatefile" style="height:50px;">
                    <svg viewBox="0 0 18 18">
                      <rect class="ql-stroke" height="10" width="12" x="3" y="4"></rect>
                      <circle class="ql-fill" cx="6" cy="7" r="1"></circle>
                      <polyline
                        class="ql-even ql-fill"
                        points="5 12 5 11 7 9 8 10 11 7 13 9 13 12 5 12"
                      ></polyline>
                    </svg>
                  </button>
                </span>
              </div>
            </quill-editor>
          </div>
        </FormItem>
        <FormItem>
          <input
            type="file"
            id="editorupload"
            accept="image"
            @change="onUploadimg"
            style="display:none;"
          >
          <Button type="primary" @click="handleSubmit('formValidate')">提交</Button>
        </FormItem>
      </i-form>
      <div class="imgShowBox" v-if="imgShow.show" v-on:click="imgShow.show = false">
        <img :src="imgShow.src" alt>
      </div>
    </div>
  </div>
</template>
<script>
import E from "wangeditor";
import { quillEditor } from "vue-quill-editor";
export default {
  name: "addGoods",
  data() {
    return {
      title: "新增商品",
      content: null,
      path: this.PATH.UPIMAGE,
      editorOption: {
        placeholder: "请输入详情页内容...",
        modules: {
          toolbar: "#toolbar"
        }
      },
      formValidate: {
        name: "",
        // tag_id: "",
        price: "",
        postage: "0",
        ku_num: "",
        // zhuli_num: "",
        // rules: "",
        detail: "",
        image_data: []
      },
      ruleValidate: {
        name: [{ required: true, message: "请填写商品标题", trigger: "blur" }],
        price: [{ required: true, message: "请正确输入价格", trigger: "blur" }],
        postage: [
          { required: true, message: "请正确输入邮费", trigger: "blur" }
        ],
        ku_num: [
          { required: true, message: "请正确输入库存", trigger: "blur" }
        ],
        detail: [
          { required: true, message: "请输入商品详情 ", trigger: "blur" }
        ]
      },
      formClassList: [],
      imgShow: {
        src: "",
        show: false
      }
    };
  },
  created() {},
  computed: {
    // 市场参考价
    formValidate_price() {
      if (this.formValidate.price === "") return "Enter number";
      this.formValidate.price = this.formValidate.price + "";
      function parseNumber(str) {
        const re = /(?=(?!)(d{3})+$)/g;
        return str.replace(/\D/g, "").replace(/...(?!$)/g, "$&,");
      }
      return parseNumber(this.formValidate.price);
    },
    // 运费
    formValidate_postage() {
      if (this.formValidate.postage === "") return "Enter number";
      function parseNumber(str) {
        const re = /(?=(?!)(d{3})+$)/g;
        return str.replace(/\D/g, "").replace(/...(?!$)/g, "$&,");
      }
      console.log(this.formValidate.postage);
      return parseNumber(this.formValidate.postage);
    }
  },
  methods: {
    clickupdatefile() {
      //点击富文本编辑器图标上传
      document.getElementById("editorupload").click();
    },
    onUploadimg(e) {
      // console.log("富文本编辑器", e);
      //上传富文本编辑器的图片
      if (e.target.files.length == 0) return;
      // console.log(e.target.files)
      // this.imgname = e.target.files[0].name;
      let reader = new FileReader();
      let that = this;
      //转base64
      reader.readAsDataURL(e.target.files[0]);
      reader.onload = function(e) {
        // console.log("哈哈哈", this.result);
        let result = this.result;
        var fd = new FormData();
        fd.append("bs4", result);
        let config = {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        };
        that.$http
          .post(that.PATH.UPLOADIMAGE, {
            type: "jpg",
            data: this.result
          })
          .then(
            success => {
              console.log("success", success);
              if (success.data.status == "0") {
                let dataurl = success.data.url;
                console.log("dataurl", dataurl);
                that.formValidate.detail =
                  that.formValidate.detail + '<img src="' + dataurl + '">';
              } else {
                that.$Modal.error({
                  title: "提示",
                  content: "上传失败，请重试"
                  // content: success.data.errmsg
                });
              }
            },
            error => {
              console.log(error);
            }
          );
      };
    },
    handleSubmit(name) {
      var that = this;
      let data = that.formValidate;
      data.postage = this.formValidate.postage * 100 + "";
      console.log(data);
      if (that.$route.query.goodsid) {
        data.goods_id = that.$route.query.goodsid;
      }
      that.$refs[name].validate(valid => {
        if (valid) {
          that.$http.post(that.PATH.GOODSUPDATE, data).then(
            success => {
              console.log("新增修改商品", success);
              if (success.data.errno == "0") {
                that.$Message.success("操作成功");
                setTimeout(() => {
                  that.$router.push({
                    name: "goodsList"
                  });
                }, 1000);
              } else {
                that.loginFailed = false;
                that.$Modal.error({
                  title: "提示",
                  content: success.data.errmsg,
                  onOk: () => {}
                });
              }
            },
            error => {}
          );
        } else {
          this.$Message.error("请完善商品信息");
        }
      });
    },
    //图片添加
    imgUpData(res, file) {
      console.log(res, file);
      this.formValidate.image_data.push({ img_url: res.img_url, is_min: 0 });
      if (this.formValidate.image_data.length == 1) {
        this.formValidate.image_data[0].is_min = 1;
      }
    },
    imgShowFun(v) {
      this.imgShow.src = v.img_url;
      this.imgShow.show = true;
    },
    imgOnFun(v) {
      for (var i = 0; i < this.formValidate.image_data.length; i++) {
        this.formValidate.image_data[i].is_min = 0;
      }
      v.is_min = 1;
    },
    imgDelFun(v) {
      this.formValidate.image_data.splice(
        this.formValidate.image_data.indexOf(v),
        1
      );
    }
  },
  mounted() {
    var that = this;
    //判断是否为修改
    console.log("that.$route.query.goodsid", that.$route.query.goodsid);
    if (that.$route.query.goodsid) {
      that.$http
        .post(that.PATH.PCGOODSDETAIL, { goods_id: that.$route.query.goodsid })
        .then(
          success => {
            console.log("商品详情", success);
            if (success.data.errno === 0) {
              this.formValidate = success.data.data[0];
              this.formValidate.postage =
                success.data.data[0].postage / 100 + "";
              this.formValidate.ku_num = this.formValidate.ku_num.toString();
              console.log(this.formValidate);

              //初始化富文本
              // var editor = new E(this.$refs.editor);
              // editor.customConfig.uploadImgShowBase64 = true;
              // editor.customConfig.onchange = html => {
              //   that.formValidate.detail = html;
              // };
              // editor.create();
              // editor.txt.html(that.formValidate.detail);
              /*for(var key in that.formValidate){
              if(success.data.data[0][key]){
                that.formValidate[key] = success.data.data[0][key]
                console.log(this.formValidate)
              }
            }*/
            }
          },
          error => {}
        );
    }
    //获取分类

    //   that.$http
    //     .post(that.PATH.TAGS, {
    //       is_all: 1,
    //       is_show: 1
    //     })
    //     .then(
    //       success => {
    //         console.log(success);
    //         if (success.data.errno == "0") {
    //           that.formClassList = success.data.data;
    //         } else {
    //           that.loginFailed = false;
    //           that.$Modal.error({
    //             title: "提示",
    //             content: success.data.errmsg,
    //             onOk: () => {}
    //           });
    //         }
    //       },
    //       error => {}
    //     );
  }
};
</script>
<style lang="scss">
#addGoods {
  height: 100%;
  padding: 20px;
  width: 100%;
  box-sizing: border-box;
  -webkit-box-sizing: border-box;
  .h1 {
    font-size: 22px;
    color: #808080;
  }
  .header {
    margin-top: 20px;
    text-align: right;
    margin-bottom: 30px;
    position: relative;
    height: 42px;
    //新增按钮
    .newbtn {
      float: right;
      text-align: left;
      margin-left: 10px;
    }
    &:before,
    &:after {
      display: table;
      line-height: 0;
      content: "";
    }
    &:after {
      clear: both;
    }
    .zhijian-new-btn {
      padding: 0 26px;
    }
  }
  .form_box {
    margin-top: 20px;
    padding: 30px 15px;
    box-sizing: border-box;
    background: #fff;
    .detail {
      width: 650px;
      padding-top: 10px;
    }
  }
  .imgSelectBox {
    width: 650px;
    height: auto;
    background: #fff;
    border: 1px solid #ccc;
    .index {
      ul {
        overflow: hidden;
        li {
          float: left;
          margin: 5px;
          width: 85px;
          height: 85px;
          overflow: hidden;
          position: relative;
          img {
            width: 100%;
          }
          .div {
            height: 0;
            top: 0;
            left: 0;
            position: absolute;
            background: rgba(0, 0, 0, 0.5);
            width: 100%;
            overflow: hidden;
            p {
              width: 33%;
              float: left;
              height: 100%;
              line-height: 85px;
              font-size: 18px;
              color: #fff;
              text-align: center;
            }
            p:hover {
              background: #979898;
            }
          }

          &:hover {
            .div {
              height: 100%;
            }
          }
        }
        .isActive {
          margin: 5px;
          border: 2px solid #1e2428;
        }
      }
    }
  }
  .imgShowBox {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba($color: #000000, $alpha: 0.5);
    z-index: 1111111;
    text-align: center;
    overflow-y: auto;
    img {
      width: 640px;
    }
  }
}
</style>
