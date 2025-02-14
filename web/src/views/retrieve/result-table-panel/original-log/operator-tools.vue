<!--
  - Tencent is pleased to support the open source community by making BK-LOG 蓝鲸日志平台 available.
  - Copyright (C) 2021 THL A29 Limited, a Tencent company.  All rights reserved.
  - BK-LOG 蓝鲸日志平台 is licensed under the MIT License.
  -
  - License for BK-LOG 蓝鲸日志平台:
  - -------------------------------------------------------------------
  -
  - Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
  - documentation files (the "Software"), to deal in the Software without restriction, including without limitation
  - the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
  - and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
  - The above copyright notice and this permission notice shall be included in all copies or substantial
  - portions of the Software.
  -
  - THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
  - LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
  - NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
  - WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
  - SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE
  -->

<template>
  <div
    :class="{ 'handle-content': true, 'fix-content': showAllHandle }"
    v-if="curHoverIndex === index"
    @mouseenter="mouseenterHandle"
    @mouseleave="mouseleaveHandle">
    <span
      v-bk-tooltips="{ content: $t('retrieve.log'), delay: 500 }"
      class="handle-card"
      v-if="showRealtimeLog && !checkIsHide('showRealtimeLog')">
      <span
        class="icon log-icon icon-handle icon-time"
        @click.stop="handleClick('realTimeLog')">
      </span>
    </span>
    <div v-if="showContextLog && !checkIsHide('showContextLog')" id="content-html">
      <span>
        <span v-if="isHaveReason" class="bk-icon icon-exclamation-circle-shape"></span>
        <span>{{contentText}}</span>
      </span>
    </div>
    <span
      v-bk-tooltips="{ allowHtml: true, content: '#content-html', delay: 500 }"
      class="handle-card"
      v-if="showContextLog && !checkIsHide('showContextLog')">
      <span
        :class="`icon log-icon icon-handle icon-document ${isHaveReason && 'is-disable'}`"
        @click.stop="handleCheckClick('contextLog')">
      </span>
    </span>
    <span
      v-bk-tooltips="{ content: $t('retrieve.monitorAlarm'), delay: 500 }"
      class="handle-card"
      v-if="showMonitorWeb && !checkIsHide('showMonitorWeb')">
      <span
        :class="`icon icon-handle log-icon icon-inform ${!monitorIsActive && 'is-disable'}`"
        @click.stop="handleCheckClick('monitorWeb')"></span>
    </span>
    <span
      v-bk-tooltips="{ content: 'WebConsole', delay: 500 }"
      class="handle-card"
      v-if="showWebConsole && !checkIsHide('showWebConsole')">
      <span
        class="icon icon-handle log-icon icon-teminal"
        @click.stop="handleClick('webConsole')"></span>
    </span>
    <span class="bk-icon icon-more handle-card icon-handle" v-if="showMoreHandle && !showAllHandle"></span>
  </div>
</template>

<script>
export default {
  props: {
    index: {
      type: Number,
      default: 0,
    },
    curHoverIndex: {
      type: Number,
      default: -1,
    },
    showRealtimeLog: {
      type: Boolean,
      default: false,
    },
    showContextLog: {
      type: Boolean,
      default: false,
    },
    showMonitorWeb: {
      type: Boolean,
      default: false,
    },
    showWebConsole: {
      type: Boolean,
      default: false,
    },
    operatorConfig: {
      type: Object,
      required: true,
    },
    handleClick: Function,
  },
  data() {
    return {
      showAllHandle: false, // hove操作区域显示全部icon
      overflowHandle: [], // 当操作按钮大于3个时 用于保存超出的icon key
    };
  },
  computed: {
    showMoreHandle() {
      const handleOptions = ['showRealtimeLog', 'showContextLog', 'showWebConsole', 'showMonitorWeb'];
      const isShowOptions = handleOptions.filter(item => this[item]);
      const isShowMore = isShowOptions.length > 3;

      if (isShowMore) {
        this.overflowHandle.push(...isShowOptions.slice(2));
      }

      return isShowMore;
    },
    monitorIsActive() {
      return this.operatorConfig?.bkmonitor.is_active;
    },
    contentText() {
      return this.operatorConfig?.contextAndRealtime.extra.reason
        ? this.operatorConfig?.contextAndRealtime.extra.reason
        : this.$t('retrieve.context');
    },
    isHaveReason() {
      return Boolean(this.operatorConfig.contextAndRealtime.extra.reason);
    },
  },
  methods: {
    mouseenterHandle() {
      this.showAllHandle = true;
    },
    mouseleaveHandle() {
      this.showAllHandle = false;
    },
    // 区分当前是否超过第3个的icon
    checkIsHide(key) {
      // 当前未hover操作区域 当前超出3个操作icon 超出第3个icon
      return !this.showAllHandle && this.showMoreHandle && this.overflowHandle.includes(key);
    },
    handleCheckClick(clickType) {
      if (clickType === 'monitorWeb' && this.monitorIsActive) return this.handleClick(clickType);
      if (clickType === 'contextLog' && !this.isHaveReason) return this.handleClick(clickType);
      return;
    },
  },
};
</script>

<style lang="scss" scoped>
  .handle-content {
    display: flex;
    position: absolute;
    right: 0;
    width: 84px;
    height: 100%;
    padding: 12px 10px;
    align-items: flex-start;
    top: 0;
    overflow: hidden;
    justify-content: flex-end;
  }

  .fix-content {
    width: auto;
    background-color: #f5f7fa;
  }

  .icon-exclamation-circle-shape {
    color: #d7473f;
  }

  .is-disable {
    /* stylelint-disable-next-line declaration-no-important */
    color: #eceef2 !important;

    /* stylelint-disable-next-line declaration-no-important */
    cursor: no-drop !important;
  }
</style>
