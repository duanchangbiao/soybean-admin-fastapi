<script setup lang="tsx">
import {NButton, NPopconfirm} from 'naive-ui';
import {$t} from "@/locales";
import {useTable, useTableOperate} from "@/hooks/common/table";
import {useAppStore} from "@/store/modules/app";
import {fetchBatchDeleteNsw, fetchDeleteNsw, fetchGetNswList} from "@/service/api";
import NswSearch from "@/views/monitor/nsw/modules/nsw-search.vue";

const appStore = useAppStore();
const {
  columns,
  columnChecks,
  data,
  getData,
  loading,
  mobilePagination,
  resetSearchParams,
  searchParams
} = useTable({
  columns: () => [
    {
      key: 'index',
      title: $t('common.index'),
      dataIndex: 'index',
      align: 'center',
      width: 64
    },
    {
      key: 'applyNumber',
      title: $t('page.business.nsw.applyNumber'),
      dataIndex: 'applyNumber',
      align: 'center',
      width: 100
    },
    {
      key: 'username',
      title: $t('page.business.nsw.username'),
      dataIndex: 'username',
      align: 'center',
      width: 150
    },
    {
      key: 'nickname',
      title: $t('page.business.nsw.nickname'),
      dataIndex: 'nickname',
      align: 'center',
      width: 150
    },
    {
      key: 'applyDate',
      title: $t('page.business.nsw.applyDate'),
      dataIndex: 'applyDate',
      align: 'center',
      width: 100
    },
    {
      key: 'applyStatus',
      title: $t('page.business.nsw.applyStatus'),
      dataIndex: 'applyStatus',
      align: 'center',
      width: 200
    },
    {
      key: 'sort',
      title: $t('page.business.nsw.sort'),
      dataIndex: 'sort',
      align: 'center',
      width: 50
    },
    {
      key: 'remark',
      title: $t('page.business.nsw.remark'),
      dataIndex: 'remark',
      align: 'center',
      width: 200
    },
    {
      key: 'ctime',
      title: $t('page.business.nsw.ctime'),
      dataIndex: 'ctime',
      align: 'center',
      width: 150
    },

    {
      key: 'operate',
      title: $t('common.operate'),
      align: 'center',
      width: 150,
      render: row => (
        <div class="flex-center gap-8px">
          <NButton type="primary" ghost size="small" onClick={() => edit(row.id)}>
            {$t('common.edit')}
          </NButton>
          <NPopconfirm onPositiveClick={() => handleDelete(row.id)}>
            {{
              default: () => $t('common.confirmDelete'),
              trigger: () => (
                <NButton type="error" ghost size="small">
                  {$t('common.delete')}
                </NButton>
              )
            }}
          </NPopconfirm>
        </div>
      )
    }
  ],
  apiFn: fetchGetNswList,
  apiParams: {
    current: 1,
    size: 10,
    applyStatus: null,
    username: null,
    applyNumber: null,
    remark: null,
  },
});

const {
  handleEdit,
  handleAdd,
  checkedRowKeys,
  onBatchDeleted,
  onDeleted,
  // closeDrawer
} = useTableOperate(data, getData);

async function handleBatchDelete() {
  // request
  const {error} = await fetchBatchDeleteNsw({ids: checkedRowKeys.value});
  if (!error) {
    onBatchDeleted();
  }
}


async function handleDelete(id: number) {
  // request
  const {error} = await fetchDeleteNsw({id});
  if (!error) {
    onDeleted();
  }
}

function edit(id: number) {
  handleEdit(id);
}
</script>

<template>
  <div class="min-h-500px flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <NswSearch v-model:model="searchParams" @reset="resetSearchParams" @search="getData"/>
    <NCard
      :title="$t('page.business.nsw.title')"
      :bordered="false"
      :body-style="{ flex: 1, overflow: 'hidden' }"
      class="flex-col-stretch sm:flex-1-hidden card-wrapper"
    >
      <template #header-extra>
        <TableHeaderOperation
          v-model:columns="columnChecks"
          :disabled-delete="checkedRowKeys.length === 0"
          :loading="loading"
          table-id="license"
          @add="handleAdd"
          @delete="handleBatchDelete"
          @refresh="getData"
        />
      </template>
      <NDataTable
        v-model:checked-row-keys="checkedRowKeys"
        :columns="columns"
        :data="data"
        size="small"
        :flex-height="!appStore.isMobile"
        :scroll-x="962"
        :loading="loading"
        remote
        :row-key="row => row.id"
        :pagination="mobilePagination"
        class="sm:h-full"
      />
    </NCard>
    <!--      <AftUpdateOperateModal-->
    <!--        v-model:visible="visible"-->
    <!--        :operate-type="operateType"-->
    <!--        :row-data="editingData"-->
    <!--        :all-pages="allPages"-->
    <!--        @submitted="getDataByPage"-->
    <!--      />-->
  </div>
</template>

<style scoped>

</style>
