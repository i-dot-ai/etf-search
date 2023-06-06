class MultiSelect extends HTMLDivElement {
  multiValues: string[] = []

  constructor() {
    super()
  }

  connectedCallback() {
    this.setup()
  }

  private createTag(value: string) {
    const tag = document.createElement('div')
    tag.classList.add('chip')
    tag.innerHTML = value

    const icon = document.createElement('gov-icon')
    icon.classList.add('close')
    icon.setAttribute('key', 'cross')
    icon.setAttribute('role', 'button')
    icon.addEventListener('click', () => this.multiRemove(value), true)
    tag.appendChild(icon)
    return tag
  }

  private createMuliSelect() {
    const multiselect = document.createElement('selectmenu')
    const source = this.querySelector('select')
    //copy all attributes from multiselect
    Array.from(source?.attributes || []).forEach((attribute) => {
      multiselect.setAttribute(
        attribute.nodeName === 'id' ? 'data-id' : attribute.nodeName,
        attribute?.nodeValue || ''
      )
    })

    const options = source?.querySelectorAll<HTMLOptionElement>('option') || []
    const button = document.createElement('div')

    button.setAttribute('slot', 'button')
    button.setAttribute('behavior', 'button')
    multiselect.prepend(button)

    options.forEach((option) => multiselect.appendChild(option))

    multiselect.addEventListener('click', (e) => {
      const option = (e.target as HTMLElement)?.closest('option')
      if (!option) return

      const newValue: string = option.value
      this.multiValues.includes(newValue)
        ? this.multiRemove(newValue)
        : this.multiAdd(newValue)
    })

    return multiselect
  }

  private multiAdd(value: string) {
    this.multiValues.push(value)
    this.multiRefreshSelectedValues()
    this.multiRefreshOptions()
  }

  private multiRemove(toRemove: string) {
    this.multiValues = this.multiValues.filter((value) => value !== toRemove)

    this.multiRefreshSelectedValues()
    this.multiRefreshOptions()
  }

  private multiRefreshSelectedValues() {
    const selectedValues = this.querySelector('.selected-values') as HTMLDivElement
    selectedValues.innerHTML = ''
    this.multiValues.forEach((value) => selectedValues.appendChild(this.createTag(value)))
  }

  private multiRefreshOptions() {
    const multiselect = this.querySelector('selectmenu') as HTMLSelectElement
    const options = multiselect.querySelectorAll('option')
    options.forEach((option) =>
      this.multiValues.includes(option.value)
        ? option.setAttribute('selected', '')
        : option.removeAttribute('selected')
    )
  }

  private setup() {
    const selectedValues = document.createElement('div')
    selectedValues.classList.add('selected-values')
    this.append(selectedValues)

    this.append(this.createMuliSelect())
  }
}

const setupMultiselect = () =>
  customElements.define('multi-select', MultiSelect, { extends: 'div' })

export default setupMultiselect
