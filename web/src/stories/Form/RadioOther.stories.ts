import type { StoryObj, Meta } from '@storybook/html'
import { Fieldset, Radio } from '../utils'

type Props = { otherLabel: string }

const meta = {
  title: 'Components/Form/Radio/Other',
  render: ({ otherLabel }) => `<div class="form-group">
  <label class="radio">
    <input type="radio" name="measure_type" value="CONTINUOUS">
    <span class="checkmark"></span>
    <span>Continuous</span>
  </label>
  <label class="radio">
    <input type="radio" name="measure_type" value="DISCRETE">
    <span class="checkmark"></span>
    <span>Discrete</span>
  </label>
  <label class="radio">
    <input type="radio" name="measure_type" value="BINARY">
    <span class="checkmark"></span>
    <span>Binary</span>
  </label>
  <label class="radio">
    <input type="radio" name="measure_type" value="ORDINAL">
    <span class="checkmark"></span>
    <span>Ordinal</span>
  </label>
  <label class="radio">
    <input type="radio" name="measure_type" value="NOMINAL">
    <span class="checkmark"></span>
    <span>Nominal</span>      
  </label>
  <label class="radio">
    <input type="radio" name="measure_type" value="OTHER" aria-controls="conditional-7b4039ab" checked>
    <span class="checkmark"></span>
    <span>Other</span>
  </label>
  <div class="form-group controller-subfield" id="conditional-7b4039ab">
    <label for="measure_type_other">${otherLabel}</label>
    <textarea placeholder="" id="measure_type_other" name="measure_type_other" class="full-width"></textarea>
  </div>

</div>`,
  argTypes: {
    otherLabel: {
      control: 'text',
      description: 'Label for the other text input',
      name: 'Other label'
    }
  },
  parameters: {
    design: {
      type: 'figma',
      url: 'https://www.figma.com/file/pN3VtobnXOlTUDK4aiZa94/i-AI-DS?type=design&node-id=32-159&t=s7R0duWzGfG8Vf2S-0'
    }
  }
} satisfies Meta<Props>

export default meta
type Story = StoryObj<Props>

export const Other: Story = {
  args: {
    otherLabel: 'Please provide more detail'
  }
}
