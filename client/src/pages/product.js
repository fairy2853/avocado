// Copyright 2022 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { LitElement, html } from 'lit';
import { getProduct } from '../utils/fetch.js';
import styles from './styles/product.js';

import '../components/product-item.js';

export class Product extends LitElement {
  static get properties() {
    return {
      productId: { type: Number },
      updateParent: { type: Function }
    };
  }

  static get styles() {
    return styles;
  }

  constructor() {
    super();
    this.state = {
      status: 'loading',
      productItem: {},
    };

    // Initial value for updateParent
    // Trigger parent components update lifecycle
    this.updateParent = () => {};
  }

  //TODO(glasnt): Unsure why this is not firstUpdated, but without it, loading different productIds 'caches'(?) 
  async updated() {
    const prevItem = this.state.productItem;
    const prevStatus = this.state.apiError?.status
    let productItem;

    // Fetch the product
    if (this.productId) {
      productItem = await getProduct(this.productId);

      this.state = {
        ...this.state,
        status: 'loaded',
        productItem,
      };

      //BUG(glasnt): going from 404 page to actual page doesn't reload.

      // Only update if the previously loaded product
      // is different than the requested product
      if (productItem?.apiError?.status != 404 && prevItem?.id !== this.productId ) {
        this.requestUpdate();
      }
      // If there was an error, make sure this is captured. 
      if (productItem?.apiError && prevStatus !== 404) { 
        this.state.apiError = productItem.apiError
        this.requestUpdate();
      }
    }
  }

  render() {
    const { status, productItem, apiError } = this.state;

    if (apiError) { 
      return html`<app-error .apiError=${apiError}></app-error>`
    }

    return  html`
      <div class="productBase">
        ${status === 'loading'
          ? html`<p>loading...</p>`
          : html`<app-product-item
              .productId="{this.productId}"
              .productItem=${productItem}
              .updateParent=${this.updateParent}
            ></app-product-item>`}
      </div>
    `;
  }
}

customElements.define('app-product', Product);
