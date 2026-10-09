import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import App from '../App.vue'
import GlobalLoader from '../components/global/GlobalLoader.vue'

describe('App', () => {
  it('mounts renders properly', () => {
    const wrapper = mount(App, {
      global: {
        plugins: [createPinia()],
      },
    })
    expect(wrapper.findComponent(GlobalLoader).exists()).toBe(true)
  })
})
