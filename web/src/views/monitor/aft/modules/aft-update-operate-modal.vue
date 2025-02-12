<script setup lang="ts">

import {$t} from "@/locales";
import {computed, reactive, ref, watch} from "vue";
import {useNaiveForm} from "@/hooks/common/form";
import {fetchAddAft, fetchUpdateAft} from "@/service/api";
import {translateOptions} from "@/utils/common";
import {aftTypeOptions, updateStatusOptions} from "@/constants/business";


defineOptions({
  name: 'AftUpdateOperateModal'
});

interface Emits {
  (e: 'submitted'): void;
}

interface Props {
  /** the type of operation */
  operateType: NaiveUI.TableOperateType;
  /** the edit row data */
  rowData?: Api.Business.AftOrAffa | null;
}

const visible = defineModel<boolean>('visible', {
  default: false
});

const emit = defineEmits<Emits>();

const props = defineProps<Props>();

function createDefaultModel(): Api.Business.AftOrAffaAddParams {
  return {
    applyNumber: "",
    applyLicense: "",
    applyStatus: "",
    accountNumber: "",
    aftType: "",
    updateStatus: "",
    remark: "",
    sort: "",
  };
};

const model: Api.Business.AftOrAffaParamsList = reactive(createDefaultModel());

const title = computed(() => {
  const titles: Record<NaiveUI.TableOperateType, string> = {
    add: $t('page.business.aft.addAft'),
    edit: $t('page.business.aft.editAft')
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
    const {error, response} = await fetchAddAft(model);
    console.log(response.data.code)
    if (!error) {
      if (response?.data.code === "0000") {
        window.$message?.success($t('common.addSuccess'));
      }
    }
  } else if (props.operateType === 'edit') {
    const {error, response} = await fetchUpdateAft(model);
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
      <NFormItem :label="$t('page.business.aft.applyNumber')" path="applyNumber">
        <NInput
          v-model:value="model.applyNumber"
          :placeholder="$t('page.business.aft.form.applyNumber')"
          :on-update-value="
            (value: string) => {
              model.applyNumber = value;
            }
          "
        />
      </NFormItem>
      <NFormItem :label="$t('page.business.aft.aftType')" path="aftType">
        <NSelect
          v-model:value="model.aftType"
          :placeholder="$t('page.business.aft.form.aftType')"
          :options="translateOptions(aftTypeOptions)"
          filterable
          clearable
        />
      </NFormItem>
      <NFormItem :label="$t('page.business.aft.applyStatus')" path="applyStatus">
        <NInput v-model:value="model.applyStatus" :placeholder="$t('page.business.aft.form.applyStatus')"/>
      </NFormItem>
      <NFormItem :label="$t('page.business.aft.accountNumber')" path="accountNumber">
        <NInput v-model:value="model.accountNumber"
                :placeholder="$t('page.business.aft.form.accountNumber')"/>
      </NFormItem>
      <NFormItem :label="$t('page.business.aft.updateStatus')" path="updateStatus">
        <NSelect
          v-model:value="model.updateStatus"
          :placeholder="$t('page.business.aft.form.updateStatus')"
          :options="translateOptions(updateStatusOptions)"
          filterable
          clearable
        />
      </NFormItem>
      <NFormItem :label="$t('page.business.aft.sort')" path="sort">
        <NInput v-model:value="model.sort" :placeholder="$t('page.business.aft.form.sort')"/>
      </NFormItem>
      <NFormItem :label="$t('page.business.aft.remark')" path="remark">
        <NInput v-model:value="model.remark"
                type="textarea"
                size="small"
                :autosize="{
                  minRows: 3,
                  maxRows: 5,
                }"
                :placeholder="$t('page.business.aft.form.remark')"/>
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
