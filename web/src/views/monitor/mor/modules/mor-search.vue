<script setup lang="ts">
import {$t} from '@/locales';
import {useNaiveForm} from "@/hooks/common/form";

const {formRef, validate, restoreValidation} = useNaiveForm();
defineOptions({
  name: 'MorSearch'
});

interface Emits {
  (e: 'reset'): void;

  (e: 'search'): void;
}

const emit = defineEmits<Emits>();

const model = defineModel<Api.Business.MorParamsList>('model', {required: true});


async function reset() {
  await restoreValidation();
  emit('reset');
}

async function search() {
  await validate();
  emit('search');
}
</script>

<template>
  <NCard :title="$t('common.search')" :bordered="false" size="small" class="card-wrapper">
    <NForm ref="formRef" :model="model" label-placement="left" :label-width="100">
      <NGrid responsive="screen" item-responsive>
        <NFormItemGi span="24 s:8 m:4" :label="$t('page.business.aft.applyStatus')" path="applyStatus"
                     class="pr-24px">
          <NInput v-model:value="model.applyStatus" :placeholder="$t('page.business.aft.form.applyStatus')"/>
        </NFormItemGi>

        <NFormItemGi span="24 s:8 m:4" :label="$t('page.business.aft.username')" path="username"
                     class="pr-24px">
          <NInput v-model:value="model.username" :placeholder="$t('page.business.aft.form.username')"/>
        </NFormItemGi>

        <NFormItemGi span="24 s:8 m:4" :label="$t('page.business.aft.applyNumber')"
                     path="applyNumber" class="pr-24px">
          <NInput v-model:value="model.applyNumber"
                  :placeholder="$t('page.business.aft.form.applyNumber')"/>
        </NFormItemGi>
        <NFormItemGi span="24 s:8 m:4" :label="$t('page.business.aft.remark')"
                     path="applyNumber" class="pr-24px">
          <NInput v-model:value="model.remark"
                  :placeholder="$t('page.business.aft.form.remark')"/>
        </NFormItemGi>

        <NFormItemGi span="24 m:8" class="pr-24px">
          <NSpace class="w-full" justify="end">
            <NButton @click="reset">
              <template #icon>
                <icon-ic-round-refresh class="text-icon"/>
              </template>
              {{ $t('common.reset') }}
            </NButton>
            <NButton type="primary" ghost @click="search">
              <template #icon>
                <icon-ic-round-search class="text-icon"/>
              </template>
              {{ $t('common.search') }}
            </NButton>
          </NSpace>
        </NFormItemGi>
      </NGrid>
    </NForm>
  </NCard>
</template>

<style scoped></style>

