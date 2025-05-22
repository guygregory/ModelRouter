# Model router for Azure AI Foundry (preview)

- Article
- <local-time format="twoDigitNumeric" datetime="2025-05-19T22:04:00.000Z" data-article-date-source="calculated" class="">05/19/2025</local-time>
- <button type="button" data-bi-name="contributors" class="contributors-button link-button">2 contributors</button>

<button id="user-feedback-button" data-test-id="conceptual-feedback-button" class="button button-sm button-clear button-primary" type="button" data-bi-name="user-feedback-button" data-user-feedback-button=""><span class="icon" aria-hidden="true"><span class="docon docon-like"></span></span><span>Feedback</span></button>

<nav id="center-doc-outline" class="doc-outline display-none-print margin-bottom-sm" data-bi-name="intopic toc" aria-label="In this article"><h2 id="ms--in-this-article" class="title is-6 margin-block-xs">In this article</h2><ol id="content-well-in-this-article-list" class="border-left padding-left-xxs"><li class=""><a href="https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/model-router#why-use-model-router">Why use model router?</a></li><li class=""><a href="https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/model-router#versioning">Versioning</a></li><li class=""><a href="https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/model-router#underlying-models">Underlying models</a></li><li class=""><a href="https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/model-router#limitations">Limitations</a></li></ol><button type="button" aria-expanded="false" data-show-more="" class="link-button font-weight-semibold font-size-sm margin-top-xxs margin-left-xs" aria-controls="content-well-in-this-article-list" data-title="Show 2 more" data-bi-name="show-more-btn"><span class="show-more-text ">Show 2 more</span></button></nav>

Model router for Azure AI Foundry is a deployable AI chat model that is trained to select the best large language model (LLM) to respond to a given prompt in real time. By evaluating factors like query complexity, cost, and performance, it intelligently routes requests to the most suitable model. Thus, it delivers high performance while saving on compute costs where possible, all packaged as a single model deployment.

https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/model-router#why-use-model-router
## Why use model router?

Model router intelligently selects the best underlying model for a given prompt to optimize costs while maintaining quality. Smaller and cheaper models are used when they're sufficient for the task, but larger and more expensive models are available for more complex tasks. Also, reasoning models are available for tasks that require complex reasoning, and non-reasoning models are used otherwise. Model router provides a single deployment and chat experience that combines the best features from all of the underlying chat models.

https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/model-router#versioning
## Versioning

Each version of model router is associated with a specific set of underlying models and their versions. This set is fixed—only newer versions of model router can expose new underlying models.

If you select **Auto-update** at the deployment step (see [Manage models](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/working-with-models?tabs=powershell#model-updates)), then your model router model automatically updates when new versions become available. When that happens, the set of underlying models also changes, which could affect the overall performance of the model and costs.

https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/model-router#underlying-models
## Underlying models

<button class="button button-clear button-sm display-flex gap-xxs"><span class="icon" aria-hidden="true"><span class="docon docon-expand color-primary"></span></span><span>Expand table</span></button>

| Model router version | Underlying models (version) |
| --- | --- |
| `2025-05-19` | GPT-4.1 (`2025-04-14`)  <br>GPT-4.1-mini (`2025-04-14`)  <br>GPT-4.1-nano (`2025-04-14`)  <br>o4-mini (`2025-04-16`) |

https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/model-router#limitations
## Limitations

https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/model-router#resource-limitations
### Resource limitations

See the [Models](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#model-router) page for the region availability and deployment types for model router.

https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/model-router#technical-limitations
### Technical limitations

See [Quotas and limits](https://learn.microsoft.com/en-us/azure/ai-services/openai/quotas-limits) for rate limit information.

 Note

The context window limit listed on the [Models](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#model-router) page is the limit of the smallest underlying model. Other underlying models are compatible with larger context windows, which means an API call with a larger context will succeed only if the prompt happens to be routed to the right model, otherwise the call will fail. To shorten the context window, you can do one of the following:

- Summarize the prompt before passing it to the model
- Truncate the prompt into more relevant parts
- Use document embeddings and have the chat model retrieve relevant sections: see [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search)

Model router accepts image inputs for [Vision enabled chats](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/gpt-with-vision) (all of the underlying models can accept image input), but the routing decision is based on the text input only.

Model router doesn't process audio input.

https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/model-router#billing-information
## Billing information

When you use model router, you're only billed for the use of the underlying models as they're recruited to respond to prompts. The model routing function itself doesn't incur any extra charges.

You can monitor the costs of your model router deployment in the Azure portal.