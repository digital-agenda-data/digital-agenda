<template>
  <nav
    v-ecl-init
    class="ecl-menu ecl-menu--group1"
    data-ecl-menu=""
    data-ecl-menu-max-lines="2"
    data-ecl-auto-init="Menu"
    aria-expanded="false"
    role="navigation"
  >
    <div class="ecl-menu__overlay" data-ecl-menu-overlay=""></div>
    <div class="ecl-container ecl-menu__container">
      <a
        class="ecl-link ecl-link--standalone ecl-menu__open"
        href="."
        data-ecl-menu-open=""
      >
        <ecl-icon icon="hamburger" size="s" />
        Menu
      </a>
      <section class="ecl-menu__inner" data-ecl-menu-inner="">
        <header class="ecl-menu__inner-header">
          <button
            class="ecl-menu__close ecl-button ecl-button--text"
            type="submit"
            data-ecl-menu-close=""
          >
            <span class="ecl-menu__close-container ecl-button__container">
              <ecl-icon
                icon="close-filled"
                size="s"
                class="ecl-button__icon ecl-button__icon--before"
              />
              <span class="ecl-button__label" data-ecl-label="true">Close</span>
            </span>
          </button>
          <div class="ecl-menu__title">Menu</div>
          <button
            data-ecl-menu-back=""
            type="submit"
            class="ecl-menu__back ecl-button ecl-button--text"
          >
            <span class="ecl-button__container">
              <ecl-icon
                icon="corner-arrow"
                rotate="270"
                size="xs"
                class="ecl-button__icon ecl-button__icon--before"
              />
              <span class="ecl-button__label" data-ecl-label="">Back</span>
            </span>
          </button>
        </header>
        <button
          class="ecl-button ecl-button--ghost ecl-menu__item ecl-menu__items-previous"
          type="button"
          data-ecl-menu-items-previous=""
          tabindex="-1"
        >
          <span class="ecl-button__container">
            <ecl-icon
              icon="corner-arrow"
              rotate="270"
              size="s"
              class="ecl-button__icon ecl-button__icon--before"
            />

            <span class="ecl-u-sr-only" data-ecl-label="true">
              Previous items
            </span>
          </span>
        </button>
        <button
          class="ecl-button ecl-button--ghost ecl-menu__item ecl-menu__items-next"
          type="button"
          data-ecl-menu-items-next=""
          tabindex="-1"
        >
          <span class="ecl-button__container">
            <ecl-icon
              icon="corner-arrow"
              rotate="90"
              class="ecl-button__icon ecl-button__icon--before"
              size="s"
            />
            <span class="ecl-u-sr-only" data-ecl-label="true">Next items</span>
          </span>
        </button>
        <ul class="ecl-menu__list" data-ecl-menu-list="">
          <template v-for="item in items" :key="item.id">
            <li
              v-if="!item.children"
              class="ecl-menu__item"
              data-ecl-menu-item=""
            >
              <ecl-link
                :to="item.link"
                :label="item.label"
                class="ecl-menu__link"
                data-ecl-menu-link=""
                variant="none"
              />
            </li>
            <li
              v-else
              class="ecl-menu__item ecl-menu__item--has-children"
              data-ecl-menu-item=""
              data-ecl-has-children=""
              aria-haspopup=""
              aria-expanded="false"
            >
              <ecl-link
                :to="item.link"
                :label="item.label"
                class="ecl-menu__link"
                data-ecl-menu-link=""
                variant="none"
              />
              <button
                class="ecl-button ecl-button--primary ecl-menu__button-caret"
                type="button"
                data-ecl-menu-caret=""
                aria-label="Access item&#x27;s children"
              >
                <span class="ecl-button__container">
                  <ecl-icon
                    icon="corner-arrow"
                    size="xs"
                    rotate="180"
                    class="ecl-button__icon ecl-button__icon--after"
                  />
                </span>
              </button>
              <div class="ecl-menu__mega" data-ecl-menu-mega="">
                <ul class="ecl-menu__sublist">
                  <li
                    v-for="child in item.children"
                    :key="child.id"
                    class="ecl-menu__subitem"
                    data-ecl-menu-subitem=""
                  >
                    <ecl-link
                      :to="item.link"
                      :label="item.label"
                      class="ecl-menu__sublink"
                      data-ecl-menu-link=""
                      variant="none"
                    />
                  </li>
                </ul>
              </div>
            </li>
          </template>
        </ul>
      </section>
    </div>
  </nav>
</template>

<script>
import EclIcon from "@/components/ecl/EclIcon.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";

/**
 * ECL Menu component, see documentation here:
 *
 * https://ec.europa.eu/component-library/ec/components/navigation/menu/usage/
 */
export default {
  name: "EclMenu",
  components: { EclLink, EclIcon },
  props: {
    /**
     * Requires an array with the following keys: id, link, label, children
     *
     * Only 2 levels supported.
     */
    items: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped></style>
