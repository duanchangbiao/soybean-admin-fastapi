<script setup lang="ts" generic="T extends Record<string, unknown>, K = never">
import { VueDraggable } from 'vue-draggable-plus';
import { $t } from '@/locales';

defineOptions({
  name: 'TableColumnSetting'
});

interface Emits {
  (e: 'updateValue'): void;
}

const emit = defineEmits<Emits>();

const columns = defineModel<NaiveUI.TableColumnCheck[]>('columns', {
  required: true
});

function updateValue() {
  emit('updateValue');
}
</script>

<template>
  <NPopover placement="bottom-end" trigger="click">
    <template #trigger>
      <NButton size="small">
        <template #icon>
          <icon-ant-design-setting-outlined class="text-icon" />
        </template>
        {{ $t('common.columnSetting') }}
      </NButton>
    </template>
    <VueDraggable v-model="columns" :animation="150" filter=".none_draggable">
      <NScrollbar class="h-100">
        <div
          v-for="item in columns"
          :key="item.key"
          class="h-36px flex-y-center rd-4px hover:(bg-primary bg-opacity-20)"
        >
          <icon-mdi-drag class="mr-8px h-full cursor-move text-icon" />
          <NCheckbox v-model:checked="item.checked" class="none_draggable flex-1" @update:checked="updateValue">
            {{ item.title }}
          </NCheckbox>
        </div>
      </NScrollbar>
    </VueDraggable>
  </NPopover>
</template>

<style scoped></style>
