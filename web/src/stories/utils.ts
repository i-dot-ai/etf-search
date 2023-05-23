import { Input, Select, Textarea } from './types'

export const createInput = ({ fullWidth, dimension, onkeyup, ...props }: Input) => {
  const input = document.createElement('input')

  for (const [key, value] of Object.entries(props)) {
    input.setAttribute(key, value?.toString() || '')
  }
  fullWidth && input.classList.add('full-width')
  !!dimension && dimension !== 'medium' && input.classList.add(dimension)
  typeof onkeyup === 'function' && input.addEventListener('keyup', onkeyup)

  return input
}

export const createSelect = ({
  fullWidth,
  disabled,
  onchange,
  optionList,
  ...props
}: Select) => {
  const select = document.createElement('select')
  for (const [key, value] of Object.entries(props)) {
    select.setAttribute(key, value?.toString() || '')
  }
  select.innerHTML = `<option>Please select</option>`
  optionList.forEach((option) => {
    const optionElement = document.createElement('option')
    optionElement.value = option
    optionElement.text = option
    select.appendChild(optionElement)
  })
  fullWidth && select.classList.add('full-width')
  disabled && select.setAttribute('disabled', 'true')

  const wrapper = document.createElement('div')
  wrapper.classList.add('select')
  wrapper.appendChild(select)

  typeof onchange === 'function' && select.addEventListener('change', onchange)

  return wrapper
}

export const createTextarea = ({ fullWidth, onkeyup, ...props }: Textarea) => {
  const textarea = document.createElement('textarea')

  for (const [key, value] of Object.entries(props)) {
    textarea.setAttribute(key, value?.toString() || '')
  }
  fullWidth && textarea.classList.add('full-width')

  typeof onkeyup === 'function' && textarea.addEventListener('keyup', onkeyup)

  return textarea
}

export * from './types'
