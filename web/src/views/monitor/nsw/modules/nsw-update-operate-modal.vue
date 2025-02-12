<script setup lang="tsx">

import {$t} from "@/locales";
import {computed, reactive, ref, watch} from "vue";
import {fetchAddNsw, fetchUpdateNsw} from "@/service/api";
import {useNaiveForm} from "@/hooks/common/form";
import {translateOptions} from "@/utils/common";
import {updateStatusOptions} from "@/constants/business";

defineOptions({
  name: 'NswUpdateOperateModal'
});


interface Emits {
  (e: 'submitted'): void;
}

interface Props {
  /** the type of operation */
  operateType: NaiveUI.TableOperateType;
  /** the edit row data */
  rowData?: Api.Business.Nsw | null;
}

const visible = defineModel<boolean>('visible', {
  default: false
});

const emit = defineEmits<Emits>();

const props = defineProps<Props>();

function createDefaultModel(): Api.Business.NswAddParams {
  return {
    applyNumber: "",
    applyStatus: "",
    accountNumber: "",
    updateStatus: "",
    remark: "",
    sort: "",
  };
};

const model: Api.Business.NswParamsList = reactive(createDefaultModel());

const title = computed(() => {
  const titles: Record<NaiveUI.TableOperateType, string> = {
    add: $t('page.business.nsw.addNsw'),
    edit: $t('page.business.nsw.editNsw')
  };
  return titles[props.operateType];
});

function closeDrawer() {
  visible.value = false;
}

// 打开弹框
function handleInitModel() {
  Object.assign(model, createDefaultModel());
  if (props.operateType === 'edit' && props.rowData) {
    console.log('props.rowData', props.rowData);
    Object.assign(model, props.rowData);
  }
}

const {formRef, validate, restoreValidation} = useNaiveForm();

async function handleSubmit() {
  await validate();
  // request

  if (props.operateType === 'add') {
    const {error, response} = await fetchAddNsw(model);
    console.log(response.data.code)
    if (!error) {
      if (response?.data.code === "0000") {
        window.$message?.success($t('common.addSuccess'));
      }
    }
  } else if (props.operateType === 'edit') {
    const {error, response} = await fetchUpdateNsw(model);
    if (!error) {
      if (response?.data.code === "0000") {
        window.$message?.success($t('common.addSuccess'));
      }
    }
  }

  closeDrawer();
  emit('submitted');
}

watch(visible, () => {
  if (visible.value) {
    handleInitModel();
    restoreValidation();
  }
});
</script>

<template>
  <NModal v-model:show="visible" preset="dialog" :title="title" class="min-w-200">
    <NForm
      ref="formRef"
      :model="model"
      label-placement="left"
      label-width="auto"
      require-mark-placement="right-hanging"
      size="medium"
      class="max-w-230"
    >
      <NFormItem :label="$t('page.business.nsw.applyNumber')" path="applyNumber">
        <NInput
          v-model:value="model.applyNumber"
          :placeholder="$t('page.business.nsw.form.applyNumber')"
          :on-update-value="
            (value: string) => {
              model.applyNumber = value;
            }
          "
        />
      </NFormItem>
      <NFormItem :label="$t('page.business.nsw.applyStatus')" path="applyStatus">
        <NInput v-model:value="model.applyStatus" :placeholder="$t('page.business.nsw.form.applyStatus')"/>
      </NFormItem>
      <NFormItem :label="$t('page.business.nsw.accountNumber')" path="accountNumber">
        <NInput v-model:value="model.accountNumber"
                :placeholder="$t('page.business.nsw.form.accountNumber')"/>
      </NFormItem>
      <NFormItem :label="$t('page.business.nsw.sort')" path="sort">
        <NInput v-model:value="model.sort" :placeholder="$t('page.business.nsw.form.sort')"/>
      </NFormItem>
      <NFormItem :label="$t('page.business.nsw.updateStatus')" path="updateStatus">
        <NSelect
          v-model:value="model.updateStatus"
          :placeholder="$t('page.business.nsw.form.updateStatus')"
          :options="translateOptions(updateStatusOptions)"
          filterable
          clearable
        />
      </NFormItem>
      <NFormItem :label="$t('page.business.nsw.remark')" path="remark">
        <NInput v-model:value="model.remark"
                type="textarea"
                size="small"
                :autosize="{
                  minRows: 3,
                  maxRows: 5,
                }"
                :placeholder="$t('page.business.nsw.form.remark')"/>
      </NFormItem>
    </NForm>
    <template #action>
      <NSpace :size="16">
        <NButton @click="closeDrawer">{{ $t('common.cancel') }}</NButton>
        <NButton type="primary" @click="handleSubmit">{{ $t('common.confirm') }}</NButton>
      </NSpace>
    </template>
  </NModal>
</template>

<style scoped>

</style>
