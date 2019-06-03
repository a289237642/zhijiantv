<template>
  <div id="goodsList">
    <div class="h1">商品列表</div>
    <div class="header">
      <Input
        search
        enter-button="搜索"
        placeholder="快速搜索"
        class="search"
        @on-search="getSearchValue"
        :v-model="val"
      />
      <Button type="primary" class="newbtn zhijian-new-btn" @click="addGoods">新增</Button>
    </div>
    <!-- 商品列表部分 -->
    <Tabs value="name1" class="tabs" size="default" @on-click="changeTabs">
      <TabPane label="全部" name="name1" class="tabpane">
        <Table :data="allData" :columns="allColumns" stripe></Table>
        <Modal v-model="modal1" draggable scrollable class-name="modal">
          <div>请确认是否{{isOn}}商品</div>
          <div class="cancle" @click="cancel">取消</div>
          <div class="zhijian-btn-confirm" @click="okIsOn">确定</div>
        </Modal>
        <Modal v-model="modal2" draggable scrollable>
          <div>请确认是否删除商品</div>
          <div class="cancle" @click="cancel">取消</div>
          <div class="zhijian-btn-confirm" @click="okIsDelete">确定</div>
        </Modal>
        <div style="margin: 10px;overflow: hidden">
          <div style="float: right;">
            <Page
              :total="total"
              :current="page"
              show-elevator
              :pageSize="pagesize"
              @on-change="changePage"
            ></Page>
          </div>
        </div>
      </TabPane>
      <TabPane label="进行中" name="name2" class="tabpane">
        <Table :data="allData" :columns="allColumns" stripe></Table>
        <Modal v-model="modal1" draggable scrollable title="Modal 1">
          <div>请确认是否下架商品</div>
        </Modal>
        <Modal v-model="modal2" draggable scrollable title="Modal 2">
          <div>请确认是否删除商品</div>
        </Modal>
        <div style="margin: 10px;overflow: hidden">
          <div style="float: right;">
            <Page
              :total="total"
              :current="page"
              show-elevator
              :pageSize="pagesize"
              @on-change="changePage"
            ></Page>
          </div>
        </div>
      </TabPane>
      <TabPane label="已下架" name="name3" class="tabpane">
        <Table :data="allData" :columns="allColumns" stripe></Table>
        <Modal v-model="modal1" draggable scrollable title="Modal 1">
          <div>请确认是否{{isOn}}商品</div>
        </Modal>
        <Modal v-model="modal2" draggable scrollable title="Modal 2">
          <div>请确认是否删除商品</div>
        </Modal>
        <div style="margin: 10px;overflow: hidden">
          <div style="float: right;">
            <Page
              :total="total"
              :current="page"
              show-elevator
              :pageSize="pagesize"
              @on-change="changePage"
            ></Page>
          </div>
        </div>
      </TabPane>
    </Tabs>
  </div>
</template>

<script>
export default {
  name: "goodsList",
  data() {
    return {
      isOn: "上架", // 1是下架状态，2是进行中（上架状态）
      tagid: "", // 分类id
      name: "name1",
      is_search: false,
      searchValue: "",
      model: "",
      goodsid: 1,
      val: "",
      page: 1,
      pagesize: 10,
      total: 50,
      modal1: false,
      modal2: false,
      categoryList: [{ name: "全部分类" }],
      allColumns: [
        {
          title: "商品描述",
          key: "goods_name",
          width: 300,
          render: (h, params) => {
            // console.log(params.row);
            return h("div", [
              h("img", {
                attrs: {
                  src: params.row.min_pic
                },
                style: {
                  width: "100px",
                  height: "70px",
                  border: "1px solid",
                  marginRight: "20px",
                  verticalAlign: "middle",
                  marginTop: "10px"
                }
              }),
              h(
                "p",
                {
                  style: {
                    width: "160px",
                    height: "55px",
                    marginTop: "-65px",
                    marginLeft: "120px",
                    overflow: "hidden",
                    marginBottom: "20px"
                  }
                },
                params.row.goods_name
              )
            ]);
          }
        },
        {
          title: "已兑换",
          key: "change_num",
          align: "center"
        },
        {
          title: "库存",
          key: "ku_num",
          align: "center"
        },
        {
          title: "创建时间",
          key: "create_time",
          width: 200,
          align: "center"
        },
        {
          title: "下单名单",
          key: "nameList",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h("Icon", {
                props: {
                  type: "ios-list-box-outline",
                  size: 32
                },
                style: {
                  textAlign: "center"
                },
                on: {
                  click: () => {
                    console.log(params.row);
                    this.$router.push({
                      name: "applicationLists",
                      params: { goodsid: params.row.goods_id }
                    });
                  }
                }
              })
            ]);
          }
        },
        {
          title: "操作",
          key: "action",
          width: 300,
          align: "center",
          render: (h, params) => {
            let isOn = "下架";
            let bgColor = "#FFC639";
            let color = "#fff";
            if (params.row.is_show == 1) {
              isOn = "下架";
              bgColor = "#fff";
              color = "#000";
            } else {
              bgColor = "#FFC639";
              isOn = "上架";
              color = "#fff";
            }
            return h("div", [
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small"
                  },
                  style: {
                    color: color,
                    marginRight: "5px",
                    background: bgColor,
                    borderColor: "#FFC639"
                  },
                  on: {
                    click: () => {
                      this.isOn = isOn;
                      this.modal1 = true;
                      this.goodsid = params.row.goods_id;
                    }
                  }
                },
                isOn
              ),
              h("Icon", {
                props: {
                  type: "ios-create-outline",
                  size: 32
                },
                style: {
                  marginRight: "5px"
                },
                on: {
                  click: () => {
                    this.$router.push({
                      name: "addGoods",
                      query: { isEdit: true, goodsid: params.row.goods_id }
                    });
                  }
                }
              }),
              h("Icon", {
                props: {
                  type: "ios-trash-outline",
                  size: 32
                },
                style: {
                  marginRight: "5px"
                },
                on: {
                  click: () => {
                    console.log(params.row);
                    this.goodsid = params.row.goods_id;
                    this._data.modal2 = true;
                  }
                }
              })
            ]);
          }
        }
      ],
      allData: []
    };
  },
  created() {
    this.getData();
  },
  methods: {
    // getTagData() {
    //   this.$http
    //     .post(this.PATH.TAGS, {
    //       is_all: 1
    //     })
    //     .then(res => {
    //       let data = res.data.data;
    //       for (let i in data) {
    //         this.categoryList.push(data[i]);
    //       }
    //     });
    // },

    /**
     * 获取列表
     */
    getData(isShow = 0) {
      // console.log("isShow", isShow);
      let params = {};
      if (isShow === 1) {
        // 上架
        params = {
          page: this.page,
          pagesize: this.pagesize,
          is_show: 1
        };
      } else if (isShow === -1) {
        // 下架
        params = {
          page: this.page,
          pagesize: this.pagesize,
          is_show: -1
        };
      } else if (isShow === 0) {
        // 全部
        params = {
          page: this.page,
          pagesize: this.pagesize
        };
      }
      this.$http.post(this.PATH.GOODSLIST, params).then(res => {
        console.log(res.data);
        if (res.data.errno == 0) {
          this.allData = res.data.data;
          this.total = res.data.count;
        } else {
          this.$Modal.error({
            width: 360,
            content: res.data.errmsg
          });
        }
      });
    },

    /**
     * 改变tab页
     */
    changeTabs(e) {
      // console.log("changeTabs", e);
      this.page = 1;
      this.is_search = false;
      if (e == "name1") {
        this.getData();
      } else if (e == "name2") {
        this.getData(1);
      } else {
        this.getData(-1);
      }
      this.name = e;
    },

    getDataAll() {
      if (this.name == "name1") {
        this.getData();
      } else if (this.name == "name2") {
        this.getData(1);
      } else {
        this.getData(-1);
      }
    },
    /**
     * 分类
     */
    getClassify(e) {
      let tagid = "";
      this.categoryList.forEach(val => {
        if (e === "全部分类") {
          tagid = "";
        } else {
          if (e == val.name) {
            tagid = val.id;
          }
        }
      });
      this.tagid = tagid;
      let params = {};
      this.getSearchDataAll(this.searchValue);
    },

    /**
     * 分页
     */
    changePage(page) {
      this.page = page;
      console.log("this.is_search", this.is_search);
      if (this.is_search) {
        this.getSearchDataAll(this.searchValue);
      } else {
        this.getDataAll();
      }
    },

    /**
     * 确定上下架
     */
    okIsOn() {
      // console.log(this.goodsid);
      this.$http
        .post(this.PATH.GOODSDOWN, {
          goods_id: this.goodsid
        })
        .then(res => {
          // console.log("上下架", res);
          this.modal1 = false;
          if (res.data.errno === 0) {
            this.getDataAll();
          }
        });
    },

    /**
     * 确定删除
     */
    okIsDelete() {
      this.$http
        .post(this.PATH.GOODSDEL, {
          goods_id: this.goodsid
        })
        .then(res => {
          console.log("删除商品", res);
          if (res.data.errno === 0) {
            this.modal2 = false;
            this.getDataAll();
          }
        });
    },

    /**
     * 对话框取消
     */
    cancel() {
      this.modal1 = false;
      this.modal2 = false;
    },

    /**
     * 新增商品
     */
    addGoods() {
      this.$router.push({ name: "addGoods" });
    },
    getSearchDataAll(e) {
      if (this.name == "name1") {
        this.getSearchList(e);
      } else if (this.name == "name2") {
        this.getSearchList(e, -1);
      } else {
        this.getSearchList(e, 1);
      }
    },
    getSearchList(e, s) {
      let that = this;
      this.$http
        .post(this.PATH.GOODSQUERY, {
          goods_name: e,
          // tag_id: that.tagid,
          page: that.page,
          pagesize: 10,
          is_show: s
        })
        .then(res => {
          console.log(res);
          if (res.data.errno === 0) {
            (that.allData = res.data.data), (that.total = res.data.count);
          }
        });
    },
    /**
     * 获取搜索框的输入值
     */
    getSearchValue(e) {
      console.log(e);
      this.is_search = true;
      this.page = 1;
      this.searchValue = e;
      this.getSearchDataAll(this.searchValue);
    }
  }
};
</script>

<style lang="scss">
#goodsList {
  height: 100%;
  padding: 20px 20px 65px 20px;
  width: 100%;
  box-sizing: border-box;
  -webkit-box-sizing: border-box;
  background: #eee;
  position: relative;
  overflow: scroll;
  .h1 {
    font-size: 22px;
    color: #808080;
  }
  .header {
    height: 50px;
    .search {
      width: 200px;
      position: absolute;
      top: 75px;
      right: 120px;
    }
    .newbtn {
      font-size: 12px;
      line-height: 10px;
      height: 32px;
      position: absolute;
      top: 75px;
      right: 20px;
    }
  }
}

.zhijian-btn-confirm {
  margin: 60px 0 0 250px;
}
.cancle {
  width: 100px;
  padding: 8px 16px;
  font-size: 14px;
  background: #eee;
  text-align: center;
  margin: 60px 0 0 120px;
  float: left;
}
.ivu-modal-content {
  box-shadow: none;
}
</style>
