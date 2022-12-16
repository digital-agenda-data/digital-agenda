export default (el, binding) => {
  el.style.visibility = binding.value ? "visible" : "hidden";
};
