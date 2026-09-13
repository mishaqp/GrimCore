import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ui/services/model_provider_config_service.dart';
import 'package:ui/widgets/conversation_model_selector.dart';

void main() {
  const byokProfile = ModelProviderProfileSummary(
    id: 'byok',
    name: 'Provider One',
    baseUrl: '',
    apiKey: '',
    customHeaders: <String, String>{},
    sourceType: 'custom',
    readOnly: false,
    ready: true,
    statusText: '',
    configured: true,
  );

  Future<void> pumpSelector(
    WidgetTester tester, {
    required ProviderModelOption model,
  }) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: ConversationModelSelectorContent(
            width: 320,
            maxHeight: 360,
            profiles: const <ModelProviderProfileSummary>[byokProfile],
            providerModelsByProfileId: <String, List<ProviderModelOption>>{
              byokProfile.id: <ProviderModelOption>[model],
            },
            currentSelection: ConversationModelSelection(
              providerProfileId: byokProfile.id,
              modelId: model.id,
            ),
            showSearchField: false,
          ),
        ),
      ),
    );
    await tester.pump();
  }

  testWidgets('shows the catalog display name and keeps the model ID tooltip', (
    tester,
  ) async {
    await pumpSelector(
      tester,
      model: const ProviderModelOption(id: 'opus-6', displayName: 'opus 6☺️'),
    );

    expect(find.text('opus 6☺️'), findsOneWidget);
    expect(find.text('opus-6'), findsNothing);
    expect(find.byTooltip('opus-6'), findsOneWidget);
  });

  testWidgets('falls back to the model ID when display name is blank', (
    tester,
  ) async {
    await pumpSelector(
      tester,
      model: const ProviderModelOption(id: 'opus-6', displayName: '   '),
    );

    expect(find.text('opus-6'), findsOneWidget);
  });

  testWidgets('one search result stays a separate accessible model button', (
    tester,
  ) async {
    final semantics = tester.ensureSemantics();
    ConversationModelSelection? selected;
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: ConversationModelSelectorContent(
            width: 320,
            maxHeight: 360,
            profiles: const [byokProfile],
            providerModelsByProfileId: const {
              'byok': [
                ProviderModelOption(id: 'GLM-5.2', displayName: 'GLM-5.2'),
              ],
            },
            onSelect: (value) => selected = value,
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();
    await tester.enterText(find.byType(TextField), 'GLM-5.2');
    await tester.pumpAndSettle();
    final model = find.bySemanticsLabel(RegExp(r'^GLM-5\.2$'));
    expect(model, findsOneWidget);
    await tester.tap(model);
    expect(selected?.providerProfileId, 'byok');
    expect(selected?.modelId, 'GLM-5.2');
    semantics.dispose();
  });

  testWidgets('current connection is reachable before other connections', (
    tester,
  ) async {
    const other = ModelProviderProfileSummary(
      id: 'other',
      name: 'Other connection',
      baseUrl: 'https://example.invalid',
      apiKey: '',
      customHeaders: {},
      sourceType: 'custom',
      readOnly: false,
      ready: true,
      statusText: '',
      configured: true,
    );
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: ConversationModelSelectorContent(
            width: 320,
            maxHeight: 360,
            profiles: const [other, byokProfile],
            currentSelection: const ConversationModelSelection(
              providerProfileId: 'byok',
              modelId: 'model',
            ),
            providerModelsByProfileId: const {
              'byok': [
                ProviderModelOption(id: 'model', displayName: 'Selected model'),
              ],
            },
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();
    expect(
      tester.getTopLeft(find.text('Provider One')).dy,
      lessThan(tester.getTopLeft(find.text('Other connection')).dy),
    );
    expect(find.text('Selected model').hitTestable(), findsOneWidget);
  });
}
