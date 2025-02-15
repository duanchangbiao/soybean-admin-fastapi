<script setup lang="tsx">
import {NButton, NPopconfirm, NTag} from 'naive-ui';
import {$t} from "@/locales";
import {useTable, useTableOperate} from "@/hooks/common/table";
import {useAppStore} from "@/store/modules/app";
import {fetchBatchDeleteMor, fetchDeleteMor, fetchGetMorList} from "@/service/api";
import MorSearch from "@/views/monitor/mor/modules/mor-search.vue";
import {morTypeRecord, updateStatusRecord} from "@/constants/business";
import MorUpdateOperateModal from "@/views/monitor/mor/modules/mor-update-operate-modal.vue";

const appStore = useAppStore();
const {
  columns,
  columnChecks,
  data,
  getData,
  loading,
  getDataByPage,
  mobilePagination,
  resetSearchParams,
  searchParams
} = useTable({
  columns: () => [
    {
      type: 'selection',
      align: 'center',
      width: 48
    },
    {
      key: 'index',
      title: $t('common.index'),
      dataIndex: 'index',
      align: 'center',
      width: 64
    },
    {
      key: 'applyNumber',
      title: $t('page.business.mor.applyNumber'),
      dataIndex: 'applyNumber',
      align: 'center',
      width: 100
    },
    {
      key: 'accountNumber',
      title: $t('page.business.mor.accountNumber'),
      dataIndex: 'accountNumber',
      align: 'center',
      width: 150
    },
    {
      key: 'nickName',
      title: $t('page.business.mor.nickName'),
      dataIndex: 'nickName',
      align: 'center',
      width: 150
    },
    {
      key: 'morType',
      title: $t('page.business.mor.morType'),
      dataIndex: 'morType',
      align: 'center',
      width: 64,
      render: row => {
        if (row.aftType === null) {
          return null;
        }

        const tagMap: Record<Api.Business.morTypeInfo, NaiveUI.ThemeColor> = {
          "mor5": 'success',
          "mor9": 'info',
        };
        const label = $t(morTypeRecord[row.morType]);
        return <NTag type={tagMap[row.morType]}>{label}</NTag>;
      }
    },
    {
      key: 'updateStatus',
      title: $t('page.business.mor.updateStatus'),
      dataIndex: 'updateStatus',
      align: 'center',
      width: 150,
      render: row => {
        if (row.updateStatus === null) {
          return null;
        }

        const tagMap: Record<Api.Business.updateStatus, NaiveUI.ThemeColor> = {
          "1": 'primary',
          "2": 'success',
          "3": 'info',
        };
        const label = $t(updateStatusRecord[row.updateStatus]);
        return <NTag type={tagMap[row.updateStatus]}>{label}</NTag>;
      }
    },
    {
      key: 'applyStatus',
      title: $t('page.business.mor.applyStatus'),
      dataIndex: 'applyStatus',
      align: 'center',
      width: 200,
      render: row => {
        if (row.aftType === null) {
          return null;
        }

        const tagMap: Record<Api.Common.monitorStatus, NaiveUI.ThemeColor> = {
          "进行中": 'info',
          "完成": 'success',
          "系统自动取消": 'warning',
          "异常": 'error'
        };
        return <NTag type={tagMap[row.applyStatus]}>{row.applyStatus}</NTag>;
      }
    },
    // {
    //   key: 'sort',
    //   title: $t('page.business.mor.sort'),
    //   dataIndex: 'sort',
    //   align: 'center',
    //   width: 50
    // },
    {
      key: 'remark',
      title: $t('page.business.mor.remark'),
      dataIndex: 'remark',
      align: 'center',
      width: 200
    },
    {
      key: 'fmtCtime',
      title: $t('page.business.mor.ctime'),
      dataIndex: 'fmtCtime',
      align: 'center',
      width: 150
    },
    {
      key: 'fmtMtime',
      title: $t('page.business.aft.mtime'),
      dataIndex: 'mtime',
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
  apiFn: fetchGetMorList,
  showTotal: true,
  apiParams: {
    current: 1,
    size: 10,
    applyStatus: null,
    accountNumber: null,
    applyNumber: null,
    morType: null,
    remark: null,
  },
});

const {
  drawerVisible,
  operateType,
  handleEdit,
  handleAdd,
  checkedRowKeys,
  onBatchDeleted,
  editingData,
  onDeleted
  // closeDrawer
} = useTableOperate(data, getData);

async function handleBatchDelete() {
  // request
  const {error} = await fetchBatchDeleteMor({ids: checkedRowKeys.value});
  if (!error) {
    onBatchDeleted();
  }
}


async function handleDelete(id: number) {
  // request
  const {error} = await fetchDeleteMor({id});
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
    <MorSearch v-model:model="searchParams" @reset="resetSearchParams" @search="getData"/>
    <NCard
      :title="$t('page.business.mor.title')"
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
    <MorUpdateOperateModal
      v-model:visible="drawerVisible"
      :operate-type="operateType"
      :row-data="editingData"
      @submitted="getDataByPage"
    />
  </div>
</template>

<style scoped>

</style>
