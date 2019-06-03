<template>
    <div id="schoolManagement">
      <input type="file" id="inputFile" accept="image/gif, image/jpeg, image/png, image/jpg" style="display:none" @change="onUpload($event)">
      <Tabs value="name1" @on-click="changeTabs">
        <TabPane label="模块一" name="name1">
          <div class="schoolManagement_container" v-if="module1">
            <div>
              <div class="schoolManagement_part" v-for="(item,index) in module1.list">
                <div>{{item.name}}</div>
                <div @click="withUpload(index,'module1')">
                  <img :src="item.url" v-if="item.url !== ''">
                </div>
                <div>
                  <Input type="text" v-model="item.val" placeholder="请输入跳转路径" :value="item.val" />
                </div>
              </div>
              <div class="schoolManagement_btn">
                <Button class="newbtn zhijian-new-btn" type="primary" @click="submitRe('module1')">提交</Button>
              </div>
            </div>
            <div>
              <img src="@/assets/images/curse_1.jpg">
            </div>
          </div>
        </TabPane>
        <TabPane label="模块二" name="name2">
          <div class="schoolManagement_container" v-if="module2">
            <div>
              <div class="schoolManagement_head">
                <div>
                  <label>模块二名称</label>
                  <Input type="text" v-model="module2.moduleName" placeholder="请输入名称" :value="module2.moduleName"/>
                </div>
              </div>
              <div class="schoolManagement_part" v-for="(item,index) in module2.list">
                <div>{{item.name}}</div>
                <div @click="withUpload(index,'module2')">
                  <img :src="item.url" v-if="item.url !== ''">
                </div>
                <div>
                  <Input type="text" v-model="item.val" placeholder="请输入跳转路径" :value="item.val" />
                </div>
              </div>
              <div class="schoolManagement_btn">
                <Button class="newbtn zhijian-new-btn" type="primary" @click="submitRe('module2')">提交</Button>
              </div>
            </div>
            <div>
              <img src="@/assets/images/curse_2.jpg">
            </div>
          </div>
        </TabPane>
        <TabPane label="模块三" name="name3">
          <div class="schoolManagement_container" v-if="module3">
            <div>
              <div class="schoolManagement_head">
                <div>
                  <label>模块三名称</label>
                  <Input type="text" v-model="module3.moduleName" placeholder="请输入名称" :value="module3.moduleName"/>
                </div>
                <div>
                  <label>查看全部&nbsp;&nbsp;&nbsp;&nbsp;</label>
                  <Input type="text" v-model="module3.path" placeholder="请输入跳转路径" :value="module3.path"/>
                </div>
              </div>
              <div class="schoolManagement_part" v-for="(item,index) in module3.list">
                <div>{{index+1}}</div>
                <div @click="withUpload(index,'module3')">
                  <img :src="item.url" v-if="item.url !== ''">
                </div>
                <div>
                  <Input type="text" v-model="item.val" placeholder="请输入跳转路径" :value="item.val" />
                </div>
                <div>
                  <i-switch v-model="item.status" @onChange="item.status=!item.status"/>
                </div>
              </div>
              <div class="schoolManagement_btn">
                <Button class="newbtn zhijian-new-btn" type="primary" @click="submitRe('module3')">提交</Button>
              </div>
            </div>
            <div>
              <img src="@/assets/images/curse_3.jpg">
            </div>
          </div>
        </TabPane>
        <TabPane label="模块四" name="name4">
          <div class="schoolManagement_container" v-if="module4">
            <div>
              <div class="schoolManagement_head">
                <div>
                  <label>模块四名称</label>
                  <Input type="text" v-model="module4.moduleName" placeholder="请输入名称" :value="module4.moduleName"/>
                </div>
                <div>
                  <label>查看全部&nbsp;&nbsp;&nbsp;&nbsp;</label>
                  <Input type="text" v-model="module4.path" placeholder="请输入跳转路径" :value="module4.path"/>
                </div>
              </div>
              <div class="schoolManagement_part" v-for="(item,index) in module4.list">
                <div>{{index+1}}</div>
                <div @click="withUpload(index,'module4')">
                  <img :src="item.url" v-if="item.url !== ''">
                </div>
                <div>
                  <Input type="text" v-model="item.val" placeholder="请输入跳转路径" :value="item.val" />
                </div>
                <div>
                  <i-switch v-model="item.status" @onChange="item.status=!item.status"/>
                </div>
              </div>
              <div class="schoolManagement_btn">
                <Button class="newbtn zhijian-new-btn" type="primary" @click="submitRe('module4')">提交</Button>
              </div>
            </div>
            <div>
              <img src="@/assets/images/curse_4.jpg">
            </div>
          </div>
        </TabPane>
        <TabPane label="模块五" name="name5">
          <div class="schoolManagement_container" v-if="module5">
            <div>
              <div class="schoolManagement_head">
                <div>
                  <label>模块五名称</label>
                  <Input type="text" v-model="module5.moduleName" placeholder="请输入名称" :value="module5.moduleName"/>
                </div>
                <div>
                  <label>查看全部&nbsp;&nbsp;&nbsp;&nbsp;</label>
                  <Input type="text" v-model="module5.path" placeholder="请输入跳转路径" :value="module5.path"/>
                </div>
              </div>
              <div class="schoolManagement_part" v-for="(item,index) in module5.list">
                <div>{{item.name}}</div>
                <div @click="withUpload(index,'module5')">
                  <img :src="item.url" v-if="item.url">
                </div>
                <div>
                  <Input type="text" v-model="item.val" placeholder="请输入跳转路径" :value="item.val" />
                </div>
              </div>
              <div class="schoolManagement_btn">
                <Button class="newbtn zhijian-new-btn" type="primary" @click="submitRe('module5')">提交</Button>
              </div>
            </div>
            <div>
              <img src="@/assets/images/curse_5.jpg">
            </div>
          </div>
        </TabPane>
      </Tabs>
    </div>
</template>

<script>
    export default {
        name: "schoolManagement",
      data() {
          return {
            module1: null,
            module2: null,
            module3: null,
            module4: null,
            module5: null,
            moduleIndex: null,
            moduleName: null,
          }
      },
      created() {
        this.getInfo(1)
      },
      methods: {
        changeTabs(name) {
          switch (name) {
            case 'name1':
              this.getInfo(1)
                  break
            case 'name2':
              this.getInfo(2)
              break
            case 'name3':
              this.getInfo(3)
              break
            case 'name4':
              this.getInfo(4)
              break
            case 'name5':
              this.getInfo(5)
              break
          }
        },
        getInfo(id) {
          this.$http.post(this.PATH.GET_PCLESSONS,{
            module_id: id
          }).then(res=>{
            if (res.data.errno === 0) {
              if (id === 1) {
                this.module1 = res.data.data
                this.module1.list[0].name = 'banner1'
                this.module1.list[1].name = 'banner2'
                this.module1.list[2].name = 'banner3'
              } else if (id === 2) {
                this.module2 = res.data.data
                this.module2.list[0].name = 'banner4'
              } else if (id === 3) {
                this.module3 = res.data.data
              } else if (id === 4) {
                this.module4 = res.data.data
              } else if (id === 5) {
                this.module5 = res.data.data
                this.module5.list[0].name = 'banner5'
                this.module5.list[1].name = 'banner6'
                this.module5.list[2].name = 'banner7'
              }
            } else {
              this.$Modal.error({
                title:'提示',
                content:res.data.errmsg
              })
            }
          })
        },
        submitInfo(data,index) {
          this.$http.post(this.PATH.EDIT_LESSONS,data).then(res=>{
            if (res.data.errno === 0) {
              this.getInfo(index)
              this.$Modal.error({
                title:'提示',
                content:'提交成功！'
              })
            } else {
              this.$Modal.error({
                title:'提示',
                content:res.data.errmsg
              })
            }
          })
        },
        withUpload(index,name) {
          this.moduleIndex = index
          this.moduleName = name
          document.getElementById('inputFile').click()
        },
        //上传图片
        onUpload(e){
          let that = this;
          let files = e.target.files || e.dataTransfer.files;
          if (!files.length) return;
          let type = e.target.files[0].type;
          if (/^image/.test(type)){
            var reads= new FileReader();
            reads.readAsDataURL(files[0]);
            reads.onload = function () {
              let fd = new FormData()
              fd.append('data', this.result)
              let config = {
                headers: {
                  'Content-Type': 'multipart/form-data'
                }
              }
              that.$http.post('/api/v1_0/uploadimage',{
                type:'jpg',
                data:this.result
              }).then(
                res => {
                  if(res.data.status=="0") {
                    if (that.moduleName === 'module1') {
                      that.module1.list[that.moduleIndex].url = res.data.url
                    } else if (that.moduleName === 'module2') {
                      that.module2.list[that.moduleIndex].url = res.data.url
                    } else if (that.moduleName === 'module3') {
                      that.module3.list[that.moduleIndex].url = res.data.url
                    } else if (that.moduleName === 'module4') {
                      that.module4.list[that.moduleIndex].url = res.data.url
                    } else if (that.moduleName === 'module5') {
                      that.module5.list[that.moduleIndex].url = res.data.url
                    }
                  }else {
                    that.$Modal.error({
                      title:'提示',
                      content: res.data.msg
                    })
                  }
                },
                error => {
                  that.$Modal.error({
                    title:'提示',
                    content:error.data.msg
                  })
                })
            }
          }
        },
        submitRe(name) {
          let data
          switch (name) {
            case 'module1':
              data = this.module1
              data.moduleId = 1
              this.submitInfo(data,1)
              break
            case 'module2':
              data = this.module2
              data.moduleId = 2
              this.submitInfo(data,2)
              break
            case 'module3':
              data = this.module3
              data.moduleId = 3
              this.submitInfo(data,3)
              break
            case 'module4':
              data = this.module4
              data.moduleId = 4
              this.submitInfo(data,4)
              break
            case 'module5':
              data = this.module5
              data.moduleId = 5
              this.submitInfo(data,5)
              break
          }
        }
      }
    }
</script>

<style lang="scss" scoped>
  #schoolManagement{
    padding: 20px;
  }
  .schoolManagement_head{
    width: 100%;
    margin: 0 auto 30px auto;
    line-height: 32px;
    font-size: 16px;
    &:after{
      content: '';
      display: block;
      clear: both;
    }
    >div{
      &:after{
        content: '';
        display: block;
        clear: both;
      }
      margin-bottom: 10px;
      >label{
        float: left;
        margin-right: 40px;
      }
      >div{
        float: left;
        width: 60%;
      }
    }
  }
  .schoolManagement_part{
    width: 100%;
    margin: 0 auto 30px auto;
    &:after{
      content: '';
      display: block;
      clear: both;
    }
    >div{
      float: left;
      line-height: 80px;
      font-size: 18px;
      &:not(:last-of-type) {
        margin-right: 20px;
      }
      &:nth-of-type(2) {
        width: 80px;
        height: 80px;
        border: 1px dashed #333;
        cursor: pointer;
        position: relative;
        >img{
          width: 105%;
          height: 105%;
          position: absolute;
          z-index: 999;
          left: -1px;
          top: -1px;
          background-color: #f0f0f0;
        }
        &:before{
          position: absolute;
          content: '';
          display: block;
          width: 10px;
          height: 2px;
          background-color: #333;
          top: 50%;
          left: 50%;
          transform: translate(-50%,-50%);
        }
        &:after{
          position: absolute;
          content: '';
          display: block;
          width: 2px;
          height: 10px;
          background-color: #333;
          top: 50%;
          left: 50%;
          transform: translate(-50%,-50%);
        }
      }
      &:nth-of-type(3) {
        width: 60%;
      }
    }
  }
  .newbtn{
    margin-bottom: 60px;
  }
  .schoolManagement_btn{
    margin: 0 auto;
    width: 20%;
    text-align: center;
  }
  .ivu-switch-checked{
    background-color: #ffc639;
    border-color: #ffc639;
  }
  .schoolManagement_container{
    width: 90%;
    margin: 20px auto auto auto;
    &:after{
      content: '';
      display: block;
      clear: both;
    }
    >div{
      &:nth-of-type(1) {
        width: 70%;
        float: left;
      }
      &:nth-of-type(2) {
        width: 30%;
        float: right;
        >img{
          width: 100%;
        }
      }
    }
  }
</style>
